import { loadProducts } from "./server_queries.js";
import { AddProductWindow } from "./add_product_module.js"
import { ShoppingCart } from "./shopping_cart_module.js"
import { UserAccountExitWindow } from "./user_account_module.js"

async function pageInit() {

    const exitAcciuntWindow = new UserAccountExitWindow();
    const addingProductModalWindow = new AddProductWindow();
    const shoppingCartModalWindow = new ShoppingCart(exitAcciuntWindow);
    const openProductCartBtn = document.getElementById('shopping-cart-button');


    if (sessionStorage.getItem('productCart') === null) {
        sessionStorage.setItem('productCart', JSON.stringify({}));
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
            newProductCardElement.productId = productId;

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
            inCartButtonElement.productId = productId;
            newProductCardElement.append(inCartButtonElement);



            addingFragment.append(newProductCardElement);
        }
    
        currentProductContainer.append(addingFragment);
    }
    sessionStorage.setItem("productInfo", JSON.stringify(newProductInfoObject));
    
    

    document.addEventListener('click', (event) => {
        const currentProductCardElement = event.target.closest('.product-card');

        if (event.target.classList.contains('in-cart-button')) {
            const currentProductId = event.target.productId;    
            addingProductModalWindow.openWindow(currentProductId);
        } else if (currentProductCardElement) {
            const currentProductId = currentProductCardElement.productId;
            window.location.href = `${window.location.origin}/site/catalog/${currentProductId}`;
        } else if (event.target === openProductCartBtn) {
            shoppingCartModalWindow.openProductCart();
        }
    });
}

pageInit();


