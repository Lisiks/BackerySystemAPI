import { createMessage } from "./messages.js"
import { LoadingWindow } from "./load_window_module.js"

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


        this.authNameInputElement = document.getElementById('auth-window-login-input');
        this.authPasswordInputElement = document.getElementById('auth-window-password-input');

        this.authNameErrorMsgElement = document.getElementById('error-auth-name-p');
        this.authPasswordErrorMsgElement = document.getElementById('error-auth-password-p');

        this.authNameInputElement.addEventListener('focus', () => {this.authNameErrorMsgElement.style.display = "none"});
        this.authPasswordInputElement.addEventListener('focus', () => {this.authPasswordErrorMsgElement.style.display = "none"});

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
                this.hideAccountExitForm();
            }
        });

        this.registerBtnElement.addEventListener('click', this.register);
        this.loginBtnElement.addEventListener('click', this.login);
    }

    showAccountExitForm() {
        this.accountWindowElement.style.display = 'flex';
        this.authWindowElement.style.display = 'flex';
        this.regWindowElement.style.display = 'none'; 


        this.regNameInputElement.value = "";
        this.regEmailInputElement.value = "";
        this.regPasswordInputElement.value = "";
        this.regAccuredCHeckBElement.checked = false;


        this.regNameErrorMsgElement.style.display = "none";
        this.regEmailErrorMsgElement.style.display = "none";
        this.regPasswordErrorMsgElement.style.display = "none";
        this.regAccuredErrorMsgElement.style.display = "none";

        this.authNameInputElement.value = "";
        this.authPasswordInputElement.value = "";

        this.authNameErrorMsgElement.style.display = 'none';
        this.authPasswordErrorMsgElement.style.display = 'none';
    }

    hideAccountExitForm() {
        this.accountWindowElement.style.display = 'none';
        this.authWindowElement.style.display = 'none';
        this.regWindowElement.style.display = 'none'; 
    }



    showErrorLabel(label, message) {
        label.textContent = message;
        label.style.display = 'block';
    }

    register = async (event) => {
        const loadWindow = new LoadingWindow();
    
        const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/;
            
        const userName = this.regNameInputElement.value;
        const userEmail = this.regEmailInputElement.value;
        const userPwd = this.regPasswordInputElement.value;

        if (userName.length < 3 || userName.length > 50) {
            this.showErrorLabel(this.regNameErrorMsgElement, 'Некорректная длина имени пользователя (необходимая длина от 3 до 50 символов)');
            loadWindow.deleteWindow();
            return;
        }

        if (!emailRegex.test(userEmail)) {
            this.showErrorLabel(this.regEmailErrorMsgElement, 'Некорректный формат email');
            loadWindow.deleteWindow();
            return;
        }

        if (userPwd.length < 8 || userPwd.length > 72) {
            this.showErrorLabel(this.regPasswordErrorMsgElement, 'Некорректная длина пароля (необходимая длина от 8 до 72 символов)');
            loadWindow.deleteWindow();
            return;
        }

        if (!this.regAccuredCHeckBElement.checked) {
            this.showErrorLabel(this.regAccuredErrorMsgElement, 'Поставте галочку для продолжения');
            loadWindow.deleteWindow();
            return;
        }

        try {
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
            const result = await rawResult.json();
            
            switch (rawResult.status) {
                case 409:
                    switch (result.detail) {
                    case "Пользователь с таким логином уже существует":
                        this.showErrorLabel(this.regNameErrorMsgElement, 'Пользователь с данным именем уже существует');
                        break;
                    case "Пользователь с такой почтой уже существует":
                        this.showErrorLabel(this.regEmailErrorMsgElement, 'Пользователь с данным email уже существует');
                        break; 
                    }
                    break;
                case 201:
                    localStorage.setItem('bearer', result.access_token);
                    this.hideAccountExitForm();
                    createMessage("Регистрация прошла успешно.", "Теперь вы можете создавать и просматривать собственные заказы.");
            }
        } catch (error) {
            createMessage("Не удалось создать заказ.", "Возможно, у вас проблемы с подключением к сети интернет.");
        }
        loadWindow.deleteWindow();

    }

    login = async(event) => {
        const loadWindow = new LoadingWindow();
        const userName = this.authNameInputElement.value;
        const userPwd = this.authPasswordInputElement.value;

        if (userName.length < 3 || userName.length > 72) {
            this.showErrorLabel(this.authNameErrorMsgElement, 'Некорректная длина имени пользователя (необходимая длина от 3 до 50 символов)');
            loadWindow.deleteWindow();
            return;
        }

        if (userPwd.length < 8 || userPwd.length > 72) {
            this.showErrorLabel(this.authPasswordErrorMsgElement, 'Некорректная длина пароля (необходимая длина от 8 до 72 символов)');
            loadWindow.deleteWindow();
            return;
        }
  
        try {
            const rawResult = await fetch(
                `${window.location.origin}/site/login/authenticate`, {
                    method: 'POST', 
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "username": userName,
                        "password": userPwd
                    })
                }
            );

            const result = await rawResult.json();

            switch (rawResult.status) {
                case 401: {
                    this.showErrorLabel(this.authNameErrorMsgElement, 'Неверный логин или пароль');
                    break;
                }
                case 403: {
                    this.showErrorLabel( this.authNameErrorMsgElement, 'Данный пользователь является заблокированным');
                    break;
                }
                case 200: {
                    localStorage.setItem('bearer', result.access_token);
                    this.hideAccountExitForm();
                    createMessage("Авторизация прошла успешно.", "Теперь вы можете создавать и просматривать собственные заказы.");
                }
            } 
        } catch (error) {
            createMessage("Не удалось создать заказ.", "Возможно, у вас проблемы с подключением к сети интернет.");
        }
        
        loadWindow.deleteWindow();
    }
}


