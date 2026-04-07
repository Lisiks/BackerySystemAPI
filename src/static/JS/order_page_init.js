import { loadProducts } from "./server_queries.js";
import { UserAccountExitWindow } from "./user_account_module.js"

class OrderPage {
    constructor() {
        this.exitAcciuntWindow = new UserAccountExitWindow();

    
        this.userNameElement = document.getElementById('order-name');
        this.userPhoneElement = document.getElementById('order-name');
        this.orderBranchElement = document.getElementById('branch-id');
        this.orderDate = document.getElementById('order-date');
        this.orderTime = document.getElementById('order-time');
        this.orderSum = document.getElementById('order-summ');

        this.errorUserNameElement = document.getElementById('error-user-name');
        this.errorUserPhoneElement = document.getElementById('error-user-phone');
        this.errorOrderBranchElement = document.getElementById('error-branch');
        this.errorOrderDate = document.getElementById('error-order-date');
        this.errorOrderTime = document.getElementById('error-order-time');
    }

    async initPage() {
        const openProductCartBtn = document.getElementById('shopping-cart-button');
        const openLikedProductsBtn = document.getElementById('liked-products-button');
        openLikedProductsBtn.style.display = 'none';
        openProductCartBtn.style.display = 'none';

        if (sessionStorage.getItem('productCart') === null) {
            sessionStorage.setItem('productCart', JSON.stringify({}));
        }

        if (localStorage.getItem('likedProducts') === null) {
            localStorage.setItem('likedProducts', JSON.stringify([]));
        }

        const newProductInfoObject = {};
        if (sessionStorage.getItem('productInfo') === null) {
            const productsInfo = await loadProducts();
            for(const categoryId in productsInfo.categories) {
                for(const productId in productsInfo.categories[categoryId]) {
                    newProductInfoObject[productId] = productsInfo.categories[categoryId][productId];
                }
            }
            sessionStorage.setItem('productInfo', JSON.stringify(newProductInfoObject));
        }

        let orderSumm = 0
        let notAvaliablePosition = [];
        const productCart = JSON.parse(sessionStorage.getItem('productCart'));
        const productInfo = JSON.parse(sessionStorage.getItem('productInfo'));
        Object.keys(productCart).forEach(productId => {
            const currentPositionInfo = productInfo[productId];
            if (!currentPositionInfo) {
                notAvaliablePosition.push(productId);
                delete productCart[productId]
            } else {
                orderSumm += currentPositionInfo.sale_price * productCart[productId].count;
            }
        });
        this.orderSum.value = orderSumm;
        sessionStorage.setItem('productCart', JSON.stringify(newProductInfoObject));


    }
}
    

const page = new OrderPage()
page.initPage();