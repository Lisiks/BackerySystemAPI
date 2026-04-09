import { loadProducts } from "./server_queries.js";
import { ShoppingCart } from "./shopping_cart_module.js"
import { UserAccountExitWindow } from "./user_account_module.js"
import { LikedProductCirtain } from "./liked_products_module.js"
import { AddProductWindow } from "./add_product_module.js"
import { EmailForm} from "./email_message_module.js"

import { LoadingWindow } from "./load_window_module.js"
import { createMessage } from "./messages.js"

async function initPage() {
    const exitAcciuntWindow = new UserAccountExitWindow();
    const shoppingCartModalWindow = new ShoppingCart(exitAcciuntWindow);
    const likedProductsModalWindow = new LikedProductCirtain();
    const addingProductModalWindow = new AddProductWindow();
    const emailForm = new EmailForm();

    const openProductCartBtn = document.getElementById('shopping-cart-button');
    const openLikedProductsBtn = document.getElementById('liked-products-button');
    const sendSupportEmailBtn = document.getElementById('send-support-mail-btn');
    

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


    openProductCartBtn.addEventListener('click', () => {
        shoppingCartModalWindow.openProductCart();
    });
    
    openLikedProductsBtn.addEventListener('click', () => {
        likedProductsModalWindow.openWindow();
    });

    sendSupportEmailBtn.addEventListener('click', emailForm.sendMessage);

    document.addEventListener('click', (event) => {   
        if (event.target.hasAttribute('data-js-in-cart-button')) {
            const currentProductId = event.target.getAttribute('productId');    
            addingProductModalWindow.openWindow(currentProductId);
        }
        else if (event.target.hasAttribute('data-js-liked-button')) {
            const productId = event.target.getAttribute('productId');
            likedProductsModalWindow.setLikedPosition(event.target, productId);
        }
    });
}

initPage();