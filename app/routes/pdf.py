from io import BytesIO
from flask import Blueprint, render_template, send_file, redirect,flash
from flask_login import login_required,current_user
from weasyprint import HTML
from datetime import datetime
import json
from ..models.quiz import TestResult

pdf_bp = Blueprint('pdf_bp', __name__)


@pdf_bp.route('/download/report/<int:result_id>/<int:report_number>')
@login_required
def download(result_id,report_number):

    if current_user.status != "admin":
        flash('Вам запрещено скачивать отчеты', 'danger')
        return redirect('/cabinet')

    result = TestResult.query.get_or_404(result_id)
    participant = result.participant


    warnings = json.loads(result.warnings_json) if result.warnings_json else []

    if warnings and warnings != ['Без особенностей']:
        recommendations = ', '.join(warnings)
    else:
        recommendations = "Рекомендован к службе. Психологический профиль в пределах нормы."

    html_content = render_template(
        'cabinet/report.html',
        result=result,report_number=report_number
    )

    pdf = HTML(string=html_content).write_pdf()

    return send_file(
        BytesIO(pdf),
        as_attachment=True,
        download_name=f"Заключение_{participant.fullname}_{datetime.now().strftime('%d.%m.%Y')}.pdf",
        mimetype='application/pdf'
    )