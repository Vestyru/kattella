document.addEventListener('DOMContentLoaded', function () {

    const button = document.querySelector('.password-toggle');
    const passwordInput = document.getElementById('passwordInput');
    const iconOpen = document.querySelector('.eye-open');
    const iconClosed = document.querySelector('.eye-closed');

    const buttonSubmit = document.querySelector('.auth-form__submit');
    const buttonSpin = document.querySelector('.animate-spin');
    const buttonText = document.querySelector('.auth-form--text');


    button.addEventListener('click', function () {
        const type = passwordInput.type === 'password' ? 'text' : 'password';
        passwordInput.type = type


        if (type === 'text') {
            iconOpen.classList.add('hidden');
            iconClosed.classList.remove('hidden');
        } else {
            iconOpen.classList.remove('hidden');
            iconClosed.classList.add('hidden');
        }
    })

    buttonSubmit.addEventListener('click', function () {
        buttonSpin.classList.add('active');
        buttonText.style.display = 'none';
    })
})