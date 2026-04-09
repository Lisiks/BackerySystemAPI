import { loadProducts } from "./server_queries.js";
import { AddProductWindow } from "./add_product_module.js"
import { ShoppingCart } from "./shopping_cart_module.js"
import { UserAccountExitWindow } from "./user_account_module.js"
import { LikedProductCirtain } from "./liked_products_module.js"
import { EmailForm} from "./email_message_module.js"

import { LoadingWindow } from "./load_window_module.js"
import { createMessage } from "./messages.js"

async function pageInit() {

    const exitAcciuntWindow = new UserAccountExitWindow();
    const addingProductModalWindow = new AddProductWindow();
    const shoppingCartModalWindow = new ShoppingCart(exitAcciuntWindow);
    const likedProductsModalWindow = new LikedProductCirtain();
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

    const productsInfo = await loadProducts();

    const newProductInfoObject = {};

    for(const categoryId in productsInfo.categories) {
        const currentProductContainer = document.querySelector(`#category-${categoryId} > .product-container`);
        const addingFragment = document.createDocumentFragment();

        for(const productId in productsInfo.categories[categoryId]) {

            const productInfoObj = productsInfo.categories[categoryId][productId];
            newProductInfoObject[productId] = productInfoObj;

            const newProductCardElement = document.createElement('div');
            newProductCardElement.classList.add('product-card');
            newProductCardElement.setAttribute('productId', productId);

            const imageElement = document.createElement('img');
            imageElement.src = productInfoObj.image_irl;
            newProductCardElement.append(imageElement);

            const productNameTextElement = document.createElement('p');
            productNameTextElement.textContent = productInfoObj.name;
            newProductCardElement.append(productNameTextElement);

            const productInfoTextElement = document.createElement('p');

            const productInfoTextPriceElement = document.createElement('span');
            productInfoTextPriceElement.textContent = `${productInfoObj.sale_price} р `;
            productInfoTextPriceElement.classList.add('product-price-span');
            productInfoTextElement.append(productInfoTextPriceElement);

            const productInfoTextWeightElement = document.createElement('span');
            productInfoTextWeightElement.textContent = `${productInfoObj.weight} г`;
            productInfoTextWeightElement.classList.add('product-weight-span');
            productInfoTextElement.append(productInfoTextWeightElement);
            newProductCardElement.append(productInfoTextElement);

            const inCartButtonElement = document.createElement('button');
            inCartButtonElement.textContent = 'В корзину';
            inCartButtonElement.classList.add('in-cart-button');
            inCartButtonElement.setAttribute('productId', productId);
            inCartButtonElement.setAttribute('data-js-in-cart-button', '')
            newProductCardElement.append(inCartButtonElement);



            addingFragment.append(newProductCardElement);
        }
    
        currentProductContainer.append(addingFragment);
    }
    sessionStorage.setItem("productInfo", JSON.stringify(newProductInfoObject));
    


    openProductCartBtn.addEventListener('click', () => {
        shoppingCartModalWindow.openProductCart();
    });
    
    openLikedProductsBtn.addEventListener('click', () => {
        likedProductsModalWindow.openWindow();
    });

    sendSupportEmailBtn.addEventListener('click', emailForm.sendMessage);

    
    document.addEventListener('click', (event) => {
        const currentProductCardElement = event.target.closest('.product-card');


        if (event.target.hasAttribute('data-js-in-cart-button')) {
            const currentProductId = event.target.getAttribute('productId');    
            addingProductModalWindow.openWindow(currentProductId);
        } else if (currentProductCardElement) {
            const currentProductId = currentProductCardElement.getAttribute('productId');
            window.location.href = `${window.location.origin}/site/catalog/${currentProductId}`;
        }  else if (event.target.hasAttribute('data-js-liked-button')) {
            const productId = event.target.getAttribute('productId');
            likedProductsModalWindow.setLikedPosition(event.target, productId);
        }
    });
}

pageInit();


