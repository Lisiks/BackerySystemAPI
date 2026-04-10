import { LoadingWindow } from "./load_window_module.js"
import { createMessage } from "./messages.js"
import { sendSupportMail } from "./server_queries.js";

export class EmailForm {
    constructor() {
        this.usernameSupportMailInput = document.getElementById('user-name-support');
        this.userEmailSupportMailInput = document.getElementById('user-email-support');
        this.mailThemeSupportMailInput = document.getElementById('message-theme-support');
        this.mailTextSupportMailInput = document.getElementById('message-text-support');
    }

    sendMessage = async () => {
        const loadWindow = new LoadingWindow();
            
        const username = this.usernameSupportMailInput.value;
        if (username.length < 3 || username.length > 50) {
            createMessage("Сообщение не было отправлено.", "Допустимая длинна имени пользователя в сообщении от 3 до 50 символов.")
            loadWindow.deleteWindow();
            return;
        }
        const userEmail = this.userEmailSupportMailInput.value;
        const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/;
        if (!emailRegex.test(userEmail)) {
            createMessage("Сообщение не было отправлено.", "Указан некорректный Email адрес.")
            loadWindow.deleteWindow();
            return;
        }
    
        const emailTheme = this.mailThemeSupportMailInput.value;
        if (emailTheme.length < 3 || emailTheme.length > 100) {
            createMessage("Сообщение не было отправлено.", "Допустимая длинна темы сообщения от 3 до 100 символов.")
            loadWindow.deleteWindow();
            return;
        }
    
        const emailText = this.mailTextSupportMailInput.value;
        if (emailText.length < 1) {
            createMessage("Сообщение не было отправлено.", "Для отправки укажите текст сообщения.")
            loadWindow.deleteWindow();
            return;
        }
    
           
        switch (await sendSupportMail(username, userEmail, emailTheme, emailText)) {
            case "ok": {
                createMessage("Успех.", "Ваше сообщение было отправлено на сервер.")
                this.usernameSupportMailInput.value = "";
                this.userEmailSupportMailInput.value = "";
                this.mailThemeSupportMailInput.value = ""
                this.mailTextSupportMailInput.value = "";
                break;
            }
            case "ServerError": {
                createMessage("Сообщение не было отправлено.", "Возникла непредвиденная ошибка, попробуйте повторить отправку позже.")
                break;
            }
            case "NetworkError": {
                createMessage("Сообщение не было отправлено.", "Проверьте подключение к сети и повторите попытку.")
            }
        }
        loadWindow.deleteWindow();
    };


}