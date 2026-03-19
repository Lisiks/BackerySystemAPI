import { loadProducts } from "./server_queries.js";

async function pageInit() {
    document.addEventListener('click', (event) => {
        const parentProductCardElement = event.target.closest('.product-card');
        if (!event.target.classList.contains('in-cart-button') && parentProductCardElement) {
            window.location.href = `${window.location.origin}/site/catalog/${parentProductCardElement.productId}`;
        }
    });


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
            inCartButtonElement.productid = productId;
            newProductCardElement.append(inCartButtonElement);



            addingFragment.append(newProductCardElement);
        }
    
        currentProductContainer.append(addingFragment);
    }
    sessionStorage.setItem("productInfo", JSON.stringify(newProductInfoObject));
}

pageInit();


