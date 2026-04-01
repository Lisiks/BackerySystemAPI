import { loadProducts } from "./server_queries.js";
import { ShoppingCart } from "./shopping_cart_module.js"
import { UserAccountExitWindow } from "./user_account_module.js"

async function initPage() {
    const exitAcciuntWindow = new UserAccountExitWindow();
    const shoppingCartModalWindow = new ShoppingCart(exitAcciuntWindow);
    const openProductCartBtn = document.getElementById('shopping-cart-button');

    const nextPhotoSliderBtnElement = document.getElementById('next-slider-button');
    const lastPhotoSliderBtnElement = document.getElementById('last-slider-button');
    const sliderImgElement = document.getElementById('slider=content-ing');

    const imageArray = ["/static/StaticImages/abci1.png", "/static/StaticImages/abci2.png", "/static/StaticImages/abci3.jpg"];
    let currentSliderImg = 0;


    if (sessionStorage.getItem('productCart') === null) {
        sessionStorage.setItem('productCart', JSON.stringify({}));
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


    document.addEventListener('click', (event) => {
        if (event.target === openProductCartBtn) {
            shoppingCartModalWindow.openProductCart();
        }

    });

    nextPhotoSliderBtnElement.addEventListener('click', () => {
        currentSliderImg = currentSliderImg === imageArray.length - 1 ? 0 : currentSliderImg + 1;
        console.log(imageArray[currentSliderImg]);
        sliderImgElement.src = imageArray[currentSliderImg];
    });

    lastPhotoSliderBtnElement.addEventListener('click', () => {
        currentSliderImg = currentSliderImg === 0 ? imageArray.length - 1 : currentSliderImg - 1;
        sliderImgElement.src = imageArray[currentSliderImg];
    });
}

initPage();









