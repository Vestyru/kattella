from flask import Blueprint, render_template, request, redirect, flash, session, jsonify
from flask_login import login_required
from ..forms import TestForm
from ..models.quiz import Questions, Participants, Answer, TestResult
from ..extensions import db
from ..utils.cattell import calculate_16pf_scores, get_profile_verdicts, convert_raw_to_sten
from datetime import datetime
import secrets
import json

participants = Blueprint('participants', __name__)


@participants.route('/', methods=['GET', 'POST'])
def quiz():
    total = db.session.query(Questions).count()
    print(total)
    form = TestForm()
    if form.validate_on_submit():
        token = secrets.token_urlsafe(32)
        participant = Participants(
            fullname=form.fullname.data,
            squad=form.squad.data,
            callsign=form.callsign.data,
            date=form.date.data,
            token=token
        )
        try:
            db.session.add(participant)
            db.session.commit()
            session['quiz_token'] = token
            session['participant_id'] = participant.id
            session['current_page'] = 0
            return redirect('/quiz')
        except Exception as e:
            db.session.rollback()
            flash(f"При отправке произошла ошибка")
            return render_template('main/index.html')
    return render_template('main/index.html',total=total, form=form)


@participants.route('/quiz', methods=['GET', 'POST'])
def show_quiz():
    if 'quiz_token' not in session or 'participant_id' not in session:
        flash('Сначала заполните регистрационную форму!', 'error')
        return redirect('/')

    participant = Participants.query.filter_by(
        id=session['participant_id'],
        token=session['quiz_token']
    ).first()

    if not participant:
        session.clear()
        flash('Сессия устарела. Зарегистрируйтесь заново.', 'error')
        return redirect('/')

    if participant.is_completed:
        session.clear()
        flash('Вы уже завершили тест!', 'info')
        return redirect('/finish')

    current_page = session.get('current_page', 0)
    questions_per_page = 25

    all_questions = Questions.query.filter_by(
        is_active=True
    ).order_by(
        Questions.id.asc()
    ).all()
    total_count = len(all_questions)
    total_pages = (total_count + questions_per_page - 1) // questions_per_page

    start_idx = current_page * questions_per_page
    end_idx = min(start_idx + questions_per_page, total_count)
    page_questions = all_questions[start_idx:end_idx]

    if request.method == 'POST':
        try:
            for question in page_questions:
                answer_value = request.form.get(f'question_{question.id}')

                if answer_value:
                    existing = Answer.query.filter_by(
                        participant_id=participant.id,
                        question_id=question.id
                    ).first()

                    if existing:
                        existing.answered_text = answer_value
                        existing.answered_at = datetime.utcnow()
                    else:
                        new_answer = Answer(
                            participant_id=participant.id,
                            question_id=question.id,
                            answered_text=answer_value,
                            answered_at=datetime.utcnow()
                        )
                        db.session.add(new_answer)
                        db.session.commit()

            if current_page + 1 < total_pages:
                session['current_page'] = current_page + 1
                return redirect('/quiz')
            else:
                participant.is_completed = True
                participant.finished_at = datetime.utcnow()
                db.session.commit()

                all_answers = Answer.query.filter_by(participant_id=participant.id).all()
                answers_list = []
                for a in all_answers:
                    answers_list.append({
                        'question_id': a.question_id,
                        'answer_text': a.answered_text
                    })

                raw_scores = calculate_16pf_scores(participant.id)
                sten_scores = convert_raw_to_sten(raw_scores)
                verdict = get_profile_verdicts(sten_scores)

                test_result = TestResult(
                    participant_id=participant.id,
                    scores_json=json.dumps(sten_scores, ensure_ascii=False),
                    group=verdict['group'],
                    warnings_json=json.dumps(verdict['warnings'], ensure_ascii=False)
                )
                db.session.add(test_result)
                db.session.commit()

                session.clear()
                return redirect('/finish')

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка: {str(e)}', 'error')
            return redirect('/quiz')

    return render_template(
        'quiz/test.html',
        questions=page_questions,
        current_page=current_page,
        total_pages=total_pages,
        questions_per_page=questions_per_page,
        start_idx=start_idx,
        participant=participant
    )


@participants.route('/api/result/<int:result_id>', methods=['GET'])
@login_required
def get_result_api(result_id):
    try:
        import json
        result = TestResult.query.get_or_404(result_id)

        scores = json.loads(result.scores_json) if result.scores_json else {}
        warnings = json.loads(result.warnings_json) if result.warnings_json else []

        return jsonify({
            'id': result.id,
            'fullname': result.participant.fullname,
            'callsign': result.participant.callsign,
            'squad': result.participant.squad,
            'date': result.created_at.strftime('%d.%m.%Y'),
            'group': result.group,
            'warnings': warnings,
            'scores': scores
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@participants.route('/api/result/<int:result_id>', methods=['DELETE'])
@login_required
def delete_result_api(result_id):
    try:
        result = TestResult.query.get_or_404(result_id)
        participant_id = result.participant_id

        Answer.query.filter_by(participant_id=participant_id).delete()
        db.session.delete(result)
        Participants.query.filter_by(id=participant_id).delete()
        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении', 'error')
        return jsonify({'success': False, 'error': str(e)}), 500


@participants.route('/finish')
def thank_you():
    return render_template('quiz/finish.html')
