export class UserAccountExitWindow {

    constructor() {
        this.accountWindowElement = document.getElementById('account-window-bg');

        this.regWindowElement = document.getElementById('registration-window');
        this.authWindowElement = document.getElementById('authorization-window');

        this.toAuthWindowBtn = document.getElementById('to-auth-window-btn');
        this.toRegWindowBtn = document.getElementById('to-reg-window-btn');

        this.registerBtnElement = document.getElementById('register-btn');
        this.loginBtnElement = document.getElementById('authentification-btn');



        this.regNameInputElement = document.getElementById('reg-window-login-input');
        this.regEmailInputElement = document.getElementById('reg-window-email-input');
        this.regPasswordInputElement = document.getElementById('reg-window-password-input');
        this.regAccuredCHeckBElement = document.getElementById('agree-checkbox');


        this.regNameErrorMsgElement = document.getElementById('error-reg-name-p');
        this.regEmailErrorMsgElement = document.getElementById('error-reg-email-p');
        this.regPasswordErrorMsgElement = document.getElementById('error-reg-password-p');
        this.regAccuredErrorMsgElement = document.getElementById('error-reg-accured-p');


        this.regNameInputElement.addEventListener('focus', () => {this.regNameErrorMsgElement.style.display = "none"});
        this.regEmailInputElement.addEventListener('focus', () => {this.regEmailErrorMsgElement.style.display = "none"});
        this.regPasswordInputElement.addEventListener('focus', () => {this.regPasswordErrorMsgElement.style.display = "none"});
        this.regAccuredCHeckBElement.addEventListener('click', () => {this.regAccuredErrorMsgElement.style.display = "none"});



        this.toAuthWindowBtn.addEventListener('click', () => {
            this.regWindowElement.style.display = 'none';
            this.authWindowElement.style.display = 'flex';
        });

        this.toRegWindowBtn.addEventListener('click', () => {
            this.authWindowElement.style.display = 'none';
            this.regWindowElement.style.display = 'flex';  
        });


        this.accountWindowElement.addEventListener('click', (event) => {
            if (event.target == this.accountWindowElement) {
                this.accountWindowElement.style.display = 'none';
            }
        });

        

        this.regNameInputElement.addEventListener('input', () => {
            if (this.length < 3 || this.length > 50) {
                this.setCustomValidity('Нет');
            }
        })

        this.registerBtnElement.addEventListener('click', async (event) => {
            event.preventDefault();

            const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/;
            
            const userName = this.regNameInputElement.value;
            const userEmail = this.regEmailInputElement.value;
            const userPwd = this.regPasswordInputElement.value;

            if (userName.length < 3 || userName.length > 50) {
                this.regNameErrorMsgElement.textContent = 'Некорректная длина имени пользователя (необходимая длина от 3 до 50 символов)';
                this.regNameErrorMsgElement.style.display = 'block';
                return;
            }

            if (!emailRegex.test(userEmail)) {
                this.regEmailErrorMsgElement.textContent = 'Некорректный формат email';
                this.regEmailErrorMsgElement.style.display = 'block'
                return;
            }

            if (userPwd.length < 8 || userPwd.length > 72) {
                this.regPasswordErrorMsgElement.textContent = 'Некорректная длина пароля (необходимая длина от 8 до 72 символов)';
                this.regPasswordErrorMsgElement.style.display = 'block'
                return;
            }


            if (!this.regAccuredCHeckBElement.checked) {
                this.regAccuredErrorMsgElement.textContent = 'Поставте галочку для продолжения';

                this.regAccuredErrorMsgElement.style.display = 'block';
                return;
            }

            const rawResult = await fetch(
                `${window.location.origin}/site/login/register`, {
                    method: 'POST', 
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "email": userEmail,
                        "username": userName,
                        "password": userPwd
                    })
                }
            );

            console.log(rawResult);

            const result = await rawResult.json();
            




            
            

            

        })
    }

    showAccountExitForm() {
        this.accountWindowElement.style.display = 'flex';
        this.authWindowElement.style.display = 'flex';
        this.regWindowElement.style.display = 'none'; 
    }
}


