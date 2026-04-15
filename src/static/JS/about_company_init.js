import { loadProducts } from "./server_queries.js";
import { ShoppingCart } from "./shopping_cart_module.js"
import { UserAccountExitWindow } from "./user_account_module.js"
import { LikedProductCirtain } from "./liked_products_module.js"
import { AddProductWindow } from "./add_product_module.js"
import { EmailForm} from "./email_message_module.js"
import { UserProfile } from "./user_profile_module.js"

async function initPage() {
    const exitAcciuntWindow = new UserAccountExitWindow();
    const shoppingCartModalWindow = new ShoppingCart(exitAcciuntWindow);
    const likedProductsModalWindow = new LikedProductCirtain();
    const addingProductModalWindow = new AddProductWindow();
    const emailForm = new EmailForm();
    const userProfile = new UserProfile();

    const openProductCartBtn = document.getElementById('shopping-cart-button');
    const openLikedProductsBtn = document.getElementById('liked-products-button');
    const openProfileBtn = document.getElementById('in-account-button');
  

    const nextPhotoSliderBtnElement = document.getElementById('next-slider-button');
    const lastPhotoSliderBtnElement = document.getElementById('last-slider-button');
    const sliderImgElement = document.getElementById('slider=content-ing');
    const sendSupportEmailBtn = document.getElementById('send-support-mail-btn');

    const imageArray = ["/static/StaticImages/abci1.png", "/static/StaticImages/abci2.png", "/static/StaticImages/abci3.jpg"];
    let currentSliderImg = 0;


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

    openProfileBtn.addEventListener('click', () => {
        userProfile.openUserProfile();
    });

    sendSupportEmailBtn.addEventListener('click', emailForm.sendMessage);

    nextPhotoSliderBtnElement.addEventListener('click', () => {
        currentSliderImg = currentSliderImg === imageArray.length - 1 ? 0 : currentSliderImg + 1;
        sliderImgElement.src = imageArray[currentSliderImg];
    });

    lastPhotoSliderBtnElement.addEventListener('click', () => {
        currentSliderImg = currentSliderImg === 0 ? imageArray.length - 1 : currentSliderImg - 1;
        sliderImgElement.src = imageArray[currentSliderImg];
    });

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









