import { loadUserOrders, exitAccount, cancelOrder } from "./server_queries.js";
import { createMessage } from "./messages.js"
import { LoadingWindow } from "./load_window_module.js"

export class UserProfile {

    constructor(userAuthWindow) {
        this.userProfileWindow = document.getElementById('user-profile-bg');
        this.userAuthWindow = userAuthWindow;
        this.accountExitBtn = document.getElementById('user-profile-exit-account-btn');
        
        this.userProfileWindow.addEventListener('click', (event) => {
            if (event.target === this.userProfileWindow ) {
                this.closeUserProfile();
            }
        });

        this.activeOrderSectionBtn = document.getElementById("active-order-section-btn");
        this.historyOrderSectionBtn = document.getElementById("history-order-section-btn");
        this.userNameElement = document.getElementById("user-profile-user-name");

        this.activeOrdersContainer = document.querySelector('.active-orders-container');
        this.historyOrdersContainer = document.querySelector('.history-orders-container');

        this.activeOrderSectionBtn.addEventListener('click', () => {
            this.activeOrdersContainer.style.display = 'flex';
            this.historyOrdersContainer.style.display = 'none';
            this.activeOrderSectionBtn.classList.add('active');
            this.historyOrderSectionBtn.classList.remove('active');
        });

        this.historyOrderSectionBtn.addEventListener('click', () => {
            this.activeOrdersContainer.style.display = 'none';
            this.historyOrdersContainer.style.display = 'flex';
            this.activeOrderSectionBtn.classList.remove('active');
            this.historyOrderSectionBtn.classList.add('active');
        });
        
        this.accountExitBtn.addEventListener('click', async () => {
            exitAccount();
            this.closeUserProfile();
        })

        document.addEventListener('click', (event) => {
            const orderCard = event.target.closest('.order-card');
            if (orderCard && !event.target.classList.contains('cancel-button')) {
                orderCard.classList.toggle('expanded');
            }

            if (event.target.classList.contains('cancel-button') && event.target.hasAttribute("orderId")) {
                this.cancelOrder(event.target.getAttribute("orderId"), orderCard);
            }
        });
    }

    async openUserProfile() {
        const loadWindow = new LoadingWindow();

        if (!localStorage.getItem('bearer')) {
            loadWindow.deleteWindow();
            this.userAuthWindow.showAccountExitForm();
        } else {
            const orderQueryResult = await loadUserOrders()
            switch (orderQueryResult) {
                case "NetWorkError": {
                    createMessage("Не удалось загрузить данные пользователя.", "Возможно, у вас проблемы с подключением к сети интернет.");
                    break;
                }
                case "AuthError": {
                    this.userAuthWindow.showAccountExitForm();
                    break;
                }
                case "ToManyAttemp": {
                    createMessage("Не удалось загрузить данные пользователя.", "Пожалуйста, повторите попытку.");
                    break;
                }
                default: {
                    this.userNameElement.textContent = orderQueryResult.username;
                    this.fillClientOrders(orderQueryResult.orders);
                    this.userProfileWindow.style.display = 'flex';
                    this.activeOrdersContainer.style.display = 'flex';
                    this.historyOrdersContainer.style.display = 'none';
                    this.activeOrderSectionBtn.classList.add('active');
                    this.historyOrderSectionBtn.classList.remove('active');
                }
            }
        }
        loadWindow.deleteWindow();
    }

    fillClientOrders(orderObject) {
        let activeOrdersHtml = "";
        let historyOrderHtml = "";


        orderObject.forEach(order => {
            let cancelOrderbtnHtml = "";
            if (order.status_name === "Оформлен") {
                cancelOrderbtnHtml = `<button class="cancel-button" orderId="${order.id}">Отменить</button>`;
            } else if (order.status_name !== "Отменен" && order.status_name !== "Завершенный") {
                cancelOrderbtnHtml = `<button class="cancel-button" disabled>Отменить</button>`;
            }
           

            let orderProductHtml = "";
            order.items.forEach(itemInfo => {
                orderProductHtml += `
                <div class="order-item">
                    <span class="item-name">${itemInfo.product_name} ${itemInfo.quantity}</span>
                    <span class="item-price">${itemInfo.total_price} р.</span>
                </div>`;
            });

            const orderHtml = `
                <div class="order-card">
                    <div class="order-header">
                        <span class="order-id">Заказ ${order.id}</span>
                        <span class="order-date">${new Date(order.created_at).toLocaleDateString()}</span>
                        
                    </div>
                    <div class="order-details">
                        
                        <div class="order-status-and-action">
                            <div class="order-sum">${order.total_amount} р.</div>
                            <div class="order-location">${order.branch_address}</div>
                            <div class="order-current-status">${order.status_name}</div>
                            ${cancelOrderbtnHtml}
                        </div>


                        <div class="order-details-dropdown">
                            <div class="dropdown-content">
                                <div class="dropdown-item-list">
                                    <span class="dropdown-title">Детали заказа:</span>
                                    ${orderProductHtml}
                                </div>
                           
                                <div class="dropdown-address">
                                    <span class="dropdown-title">Адрес доставки:</span>
                                    <p class="address-text">${order.branch_address}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;

            if (order.status_name === "Отмененный" || order.status_name === "Завершенный") {
                historyOrderHtml += orderHtml;
            } else {
                activeOrdersHtml += orderHtml;
            }
            
        });

        this.activeOrdersContainer.innerHTML = activeOrdersHtml;
        this.historyOrdersContainer.innerHTML = historyOrderHtml;
    }

    async cancelOrder(orderId, orderCardElement) {
        const loadingWindow = new LoadingWindow();

        if (!localStorage.getItem('bearer')) {
            this.userAuthWindow.showAccountExitForm();
            loadingWindow.deleteWindow();
            return;
        }


        const cancelOrderResult = await cancelOrder(orderId);
        switch (cancelOrderResult) {
            case "AuthError": {
                this.userAuthWindow.showAccountExitForm();
                break;
            }
            case "IncorrectOrderError": {
                createMessage("Не удалось отменить заказ.", "Возможно он был удален или начал готовиться.");
                break;
            }
            default: {
                orderCardElement.remove();
                orderCardElement.querySelector(".cancel-button").remove();
                orderCardElement.querySelector(".order-current-status").textContent = 'Отмененный';
                this.historyOrdersContainer.prepend(orderCardElement);

                createMessage("Успех.", "Заказ успешно отменен.");
            }
        }
        loadingWindow.deleteWindow();
    }

    closeUserProfile() {
        this.userProfileWindow.style.display = 'none';
    }
}