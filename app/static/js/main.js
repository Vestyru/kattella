document.addEventListener('DOMContentLoaded', function () {

    /*input password*/
    const button = document.querySelector('.password-toggle');
    const passwordInput = document.getElementById('passwordInput');
    const iconOpen = document.querySelector('.eye-open');
    const iconClosed = document.querySelector('.eye-closed');

    /*spin login*/
    const buttonSubmit = document.querySelector('.auth-form__submit');
    const buttonSpin = document.querySelector('.animate-spin');
    const buttonText = document.querySelector('.auth-form--text');

    /*spin quiz*/
    const questionButton = document.querySelector('.question-screen__button');
    const questionText = document.querySelector('.question-screen-text');

    if (button && passwordInput && iconOpen && iconClosed) {
        button.addEventListener('click', function () {
            const type = passwordInput.type === 'password' ? 'text' : 'password';
            passwordInput.type = type;

            if (type === 'text') {
                iconOpen.classList.add('hidden');
                iconClosed.classList.remove('hidden');
            } else {
                iconOpen.classList.remove('hidden');
                iconClosed.classList.add('hidden');
            }
        });
    }

    if (buttonSubmit && buttonSpin && buttonText) {
        buttonSubmit.addEventListener('click', function () {
            buttonSpin.classList.add('active');
            buttonText.style.display = 'none';
        });
    }


    if (questionButton && buttonSpin && questionText) {
        questionButton.addEventListener('click', function () {
            buttonSpin.classList.add('active');
            questionText.style.display = 'none';
        });
    }

});