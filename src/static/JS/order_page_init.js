import { loadProducts } from "./server_queries.js";
import { UserAccountExitWindow } from "./user_account_module.js"
import { createOrder } from "./server_queries.js"
import { LoadingWindow } from "./load_window_module.js"
import { createMessage } from "./messages.js"
import { EmailForm} from "./email_message_module.js"
import { UserProfile } from "./user_profile_module.js"

class OrderPage {
    constructor() {
        this.exitAccountWindow = new UserAccountExitWindow();
        this.emailForm = new EmailForm();
        this.userProfile = new UserProfile();

    
        this.userNameElement = document.getElementById('order-name');
        this.userPhoneNumberElement = document.getElementById('order-phone-number');
        this.userPhoneCountryCodeElement = document.getElementById('order-phone-country-code');
        this.orderBranchElement = document.getElementById('branch-id');
        this.orderDate = document.getElementById('order-date');
        this.orderTime = document.getElementById('order-time');
        this.orderComment = document.getElementById('user-comment');
        this.orderSum = document.getElementById('order-summ');
        this.makeOrderBtn = document.getElementById('create-order-button');

        this.errorUserNameElement = document.getElementById('error-user-name');
        this.errorUserPhoneElement = document.getElementById('error-user-phone');
        this.errorOrderBranchElement = document.getElementById('error-branch');
        this.errorOrderDate = document.getElementById('error-order-date');
        this.errorOrderTime = document.getElementById('error-order-time');
    }

    async initPage() {
        const openProductCartBtn = document.getElementById('shopping-cart-button');
        const openLikedProductsBtn = document.getElementById('liked-products-button');
        const sendSupportEmailBtn = document.getElementById('send-support-mail-btn');
        const openProfileBtn = document.getElementById('in-account-button');
        openLikedProductsBtn.style.display = 'none';
        openProductCartBtn.style.display = 'none';


        if (sessionStorage.getItem('productCart') === null) {
            sessionStorage.setItem('productCart', JSON.stringify({}));
        }

        if (localStorage.getItem('likedProducts') === null) {
            localStorage.setItem('likedProducts', JSON.stringify([]));
        }

        
        if (sessionStorage.getItem('productInfo') === null) {
            const newProductInfoObject = {};
            const productsInfo = await loadProducts();
            for(const categoryId in productsInfo.categories) {
                for(const productId in productsInfo.categories[categoryId]) {
                    newProductInfoObject[productId] = productsInfo.categories[categoryId][productId];
                }
            }
            sessionStorage.setItem('productInfo', JSON.stringify(newProductInfoObject));
        }

        let orderSumm = 0
        let allPositionAvaliable = true;
        const productCart = JSON.parse(sessionStorage.getItem('productCart'));
        const productInfo = JSON.parse(sessionStorage.getItem('productInfo'));
        Object.keys(productCart).forEach(productId => {
            const currentPositionInfo = productInfo[productId];
            if (!currentPositionInfo) {
                delete productCart[productId];
                allPositionAvaliable = false;
            } else {
                orderSumm += currentPositionInfo.sale_price * productCart[productId].count;
            }
        });
        this.orderSum.textContent = `Итого: ${orderSumm.toFixed(2)}`;
        sessionStorage.setItem('productCart', JSON.stringify(productCart));

        if (Object.keys(productCart).length === 0) {
            createMessage("Корзина пуста.", "К сожалению, все выбранные вами товары в данный момент недоступны (или вы зашли в новой сессии)!");
        } else if (!allPositionAvaliable) {
            createMessage("Изменение заказа.", "К сожалению, часть выбранных вами позиций оказалась недоступной!");
        }

        this.makeOrderBtn.addEventListener('click', this.makeOrder);
        this.userNameElement.addEventListener('focus', () => {this.errorUserNameElement.style.display = 'none'});
        this.userPhoneNumberElement.addEventListener('focus', () => {this.errorUserPhoneElement.style.display = 'none'});
        this.userPhoneCountryCodeElement.addEventListener('focus', () => {this.errorUserPhoneElement.style.display = 'none'});
        this.orderBranchElement.addEventListener('focus', () => {this.errorOrderBranchElement.style.display = 'none'});
        this.orderDate.addEventListener('focus', () => {this.errorOrderDate.style.display = 'none'});
        this.orderTime.addEventListener('focus', () => {this.errorOrderTime.style.display = 'none'});

        sendSupportEmailBtn.addEventListener('click', this.emailForm.sendMessage);

        openProfileBtn.addEventListener('click', () => {
            this.userProfile.openUserProfile();
        });
    }

    showlabelError(label, message) {
        label.textContent = message;
        label.style.display = 'block';
    }
    
    makeOrder = async(event) => {
        const loadWindow = new LoadingWindow();

        const username = this.userNameElement.value;
        if (username.length < 3 || username.length > 50) {
            this.showlabelError(this.errorUserNameElement, "Некорретная длинна имени пользователя! Она должна составлять не менее 3 и не более 50 символов.");
            loadWindow.deleteWindow(); 
            return;
        }

        const userPhoneNumber = this.userPhoneNumberElement.value;
        const phoneRegex = /\d{10}/;
        if (!phoneRegex.test(userPhoneNumber)) {
            this.showlabelError(this.errorUserPhoneElement, "Некорретный номер телефона! Он должен состоять из 10 цифр.");
            loadWindow.deleteWindow(); 
            return;
        }
        const fullPhoneNumber = this.userPhoneCountryCodeElement.value + userPhoneNumber;

        const selectedBranchId = this.orderBranchElement.value;
        if (selectedBranchId === '_') {
            this.showlabelError(this.errorOrderBranchElement, "Пожалуйста укажите адрес пекарни для самовывоза!");
            loadWindow.deleteWindow();
            return;
        }

        const selectedDateStr = this.orderDate.value;
        if  (!selectedDateStr) {
            this.showlabelError(this.errorOrderDate, "Пожалуйста укажите дату, к которой заказ должен быть завершен!");
            loadWindow.deleteWindow();
            return;
        }

        if (Math.abs(new Date() - new Date(selectedDateStr)) / (1000 * 60 * 60 * 24) < 2) {
            this.showlabelError(this.errorOrderDate, "Дата, к которой заказ должен быть завершен, должна превышать текущую не менее чем на 2 дня!");
            loadWindow.deleteWindow();
            return;
        }
      
        const selectedTimeStr = this.orderTime.value;
        if (!selectedTimeStr) {
            this.showlabelError(this.errorOrderTime, "Пожалуйста укажите время, к которому заказ должен быть завершен!");
            loadWindow.deleteWindow();
            return;
        }
        const fullOrderDateStr = `${selectedDateStr}T${selectedTimeStr}:00`;

        const commentStr = this.orderComment.value;

        const orderProductsInfo = JSON.parse(sessionStorage.getItem("productCart"));
        if (Object.keys(orderProductsInfo).length === 0) {
            createMessage("Корзина пуста.", "К сожалению, все выбранные вами товары в данный момент недоступны (или вы зашли в новой сессии)!");
            loadWindow.deleteWindow(); 
            return;
        }
        const productArray = [];
        const productCart = JSON.parse(sessionStorage.getItem('productCart'));
        Object.keys(orderProductsInfo).forEach((productId) => {
            const currentProdutcRecord = {};
            currentProdutcRecord.product_id = productId;
            currentProdutcRecord.quantity = productCart[productId].count;
            productArray.push(currentProdutcRecord);
        });


        const accessToken = localStorage.getItem("bearer");
        if (!accessToken) {
            this.exitAccountWindow.showAccountExitForm();
            loadWindow.deleteWindow(); 
            return;
        }

        const result = await createOrder(username, fullPhoneNumber, productArray, selectedBranchId, commentStr, fullOrderDateStr);
        
        switch (result) {
            case "Created": {
                sessionStorage.setItem("productCart", JSON.stringify({}));
                window.location.href = `${window.location.origin}/site/new_order/success`;
                break;
            }
            case "UnavaliableProduct": {
                createMessage("Не удалось создать заказ.", "В вашем заказе оказался ряд недоступных позиций. Они были удалены из корзины. Обновите страницу для пересчета стоимости заказа.");
                break;
            };

            case "UncorrectBranch": {
                createMessage("Не удалось создать заказ.", "Выбранный филиал для самовывоза в данный момент недоступен.");
                break;
            }
            case "NetWorkError": {
                createMessage("Не удалось создать заказ.", "Возможно, у вас проблемы с подключением к сети интернет.");
                break;
            }
            case "AuthError": {
                this.exitAccountWindow.showAccountExitForm();
                break;
            }
            case "ToManyAttemp": {
                createMessage("Не удалось создать заказ.", "Пожалуйста, повторите попытку.");
                break;
            }
            default: console.log(result);
        }      
        loadWindow.deleteWindow();  
    }
}
    

const page = new OrderPage()
page.initPage();