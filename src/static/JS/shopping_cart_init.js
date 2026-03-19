const shoppingCartWindowElement = document.getElementById('black-shopping-cart-bg');
const shoppingCartProductContainerElement =document.getElementById('shoping-cart-products-block');
const shoppingCartOpenBtnElement = document.getElementById('shopping-cart-button');
const shoppingCartPticeP = document.getElementById('shoping-cart-price-p');
const closeCartButtonElement = document.getElementById("close-cart-button");


function fillProductCart() {
    const productCartData = JSON.parse(sessionStorage.getItem('productCart'));
    const productInfoData = JSON.parse(sessionStorage.getItem('productInfo'));

    const addingProductBlock = document.createDocumentFragment();

    let allPrice = 0;
    for(const productId in productCartData) {
        const productInfoObj = productInfoData[productId];
        const productCartInfoObj = productCartData[productId];
        allPrice += productInfoObj.sale_price * productCartInfoObj.count;


        const newProductInCartElement = document.createElement('div');
        newProductInCartElement.classList.add('product-in-cart');
        newProductInCartElement.id = `product-cart-position-${productId}`;

        const productImageElement = document.createElement('img');
        productImageElement.src = productInfoObj.image_irl;
        newProductInCartElement.append(productImageElement);

        const productInCartInfoElement = document.createElement('div');
        productInCartInfoElement.classList.add('product-in-cart-info');

        const productNamePElement = document.createElement('p');
        productNamePElement.classList.add('product-name');
        productNamePElement.textContent = productInfoObj.name;
        productInCartInfoElement.append(productNamePElement);

        const productWeightPElement = document.createElement('p');
        productWeightPElement.classList.add('product-weight');
        productWeightPElement.textContent = `${productInfoObj.weight} г`;
        productInCartInfoElement.append(productWeightPElement);

        const productPricePElement = document.createElement('p');
        productPricePElement.classList.add('product-price');
        productPricePElement.id = `product-cart-position-price-p-${productId}`;
        productPricePElement.textContent = `${(productInfoObj.sale_price * productCartInfoObj.count).toFixed(2)} р`;
        productInCartInfoElement.append(productPricePElement);

        newProductInCartElement.append(productInCartInfoElement);


        const productInCartCountPlaceElement = document.createElement('div');
        productInCartCountPlaceElement.classList.add('product-in-cart-count');


        const decrementButtonElement = document.createElement('button');
        decrementButtonElement.textContent = '-';
        decrementButtonElement.productid = productId;
        decrementButtonElement.classList.add('decrement-position-cart-button');
        productInCartCountPlaceElement.append(decrementButtonElement);

        const productPositionCountElement = document.createElement('p');
        productPositionCountElement.textContent = productCartInfoObj.count;
        productPositionCountElement.id = `product-cart-position-count-p-${productId}`;
        productInCartCountPlaceElement.append(productPositionCountElement);

        const incrementButtonElement = document.createElement('button');
        incrementButtonElement.textContent = '+';
        incrementButtonElement.productid = productId;
        incrementButtonElement.classList.add('increment-position-cart-button');
        productInCartCountPlaceElement.append(incrementButtonElement);

        newProductInCartElement.append(productInCartCountPlaceElement);

        const productPositionChangeButtonsElement = document.createElement('div');
        productPositionChangeButtonsElement.classList.add('product-in-cart-change-button');

        const likePositionButtonElement = document.createElement('button');
        likePositionButtonElement.classList.add('liked-position-button');
        productPositionChangeButtonsElement.append(likePositionButtonElement);

        const deletePositionButtonElement = document.createElement('button');
        deletePositionButtonElement.classList.add('delete-position-button');
        deletePositionButtonElement.productid = productId;
        productPositionChangeButtonsElement.append(deletePositionButtonElement);

        newProductInCartElement.append(productPositionChangeButtonsElement);

        addingProductBlock.append(newProductInCartElement);
    }
    shoppingCartProductContainerElement.append(addingProductBlock);
    shoppingCartPticeP.textContent = `${allPrice.toFixed(2)} р`;
}

function incrementCartPosition(productId) {
    const productInfoObj = JSON.parse(sessionStorage.getItem('productInfo'))[productId];

    const productCartInfo = JSON.parse(sessionStorage.getItem('productCart'));
    productCartInfo[productId].count++;
    sessionStorage.setItem('productCart', JSON.stringify(productCartInfo));

    const productCartPositionContainerCountObject = document.getElementById(`product-cart-position-count-p-${productId}`);
    productCartPositionContainerCountObject.textContent = parseInt(productCartPositionContainerCountObject.textContent) + 1;

    const productCartPositionContainerPriceObject = document.getElementById(`product-cart-position-price-p-${productId}`);
    const currentProductPrice = parseFloat(productCartPositionContainerPriceObject.textContent) + productInfoObj.sale_price;
    productCartPositionContainerPriceObject.textContent = `${(currentProductPrice).toFixed(2)} р`;

    const allOrderPrice = parseFloat(shoppingCartPticeP.textContent) + productInfoObj.sale_price;
    shoppingCartPticeP.textContent = `${(allOrderPrice).toFixed(2)} р`;
}

function decrementCartPosition(productId) {
    const productInfoObj = JSON.parse(sessionStorage.getItem('productInfo'))[productId];

    const productCartInfo = JSON.parse(sessionStorage.getItem('productCart'));

    if (productCartInfo[productId].count === 1) {
        return 0;
    }
    productCartInfo[productId].count--;
    sessionStorage.setItem('productCart', JSON.stringify(productCartInfo));

    const productCartPositionContainerCountObject = document.getElementById(`product-cart-position-count-p-${productId}`);
    productCartPositionContainerCountObject.textContent = parseInt(productCartPositionContainerCountObject.textContent) - 1;

    const productCartPositionContainerPriceObject = document.getElementById(`product-cart-position-price-p-${productId}`);
    const currentProductPrice = parseFloat(productCartPositionContainerPriceObject.textContent) - productInfoObj.sale_price;
    productCartPositionContainerPriceObject.textContent = `${(currentProductPrice).toFixed(2)} р`;

    const allOrderPrice = parseFloat(shoppingCartPticeP.textContent) - productInfoObj.sale_price;
    shoppingCartPticeP.textContent = `${(allOrderPrice).toFixed(2)} р`;
}

function deleteCartPosition(productId) {
    const productCartInfo = JSON.parse(sessionStorage.getItem('productCart'));
    const productInfoObj = JSON.parse(sessionStorage.getItem('productInfo'))[productId];
    const productPositionPrice = productCartInfo[productId].count * productInfoObj.sale_price;

    delete productCartInfo[productId];
    sessionStorage.setItem('productCart', JSON.stringify(productCartInfo));

    const productPositionCartElement = document.getElementById(`product-cart-position-${productId}`);
    productPositionCartElement.remove();

    const allOrderPrice = parseFloat(shoppingCartPticeP.textContent) - productPositionPrice;
    shoppingCartPticeP.textContent = `${(allOrderPrice).toFixed(2)} р`;

}


function pageInit() {
    document.addEventListener('click', (event) => {
        if (event.target === shoppingCartOpenBtnElement) {
            shoppingCartWindowElement.style.display = 'block';
            fillProductCart();
        } else if (event.target === closeCartButtonElement || event.target === shoppingCartWindowElement) {
            shoppingCartWindowElement.style.display = 'none';
            shoppingCartProductContainerElement.replaceChildren();
        } else if (event.target.classList.contains('increment-position-cart-button')) {
            const currentProductId = event.target.productid;
            incrementCartPosition(currentProductId);
        } else if (event.target.classList.contains('decrement-position-cart-button')) {
            const currentProductId = event.target.productid;
            decrementCartPosition(currentProductId);
        } else if (event.target.classList.contains('delete-position-button')) {
            const currentProductId = event.target.productid;
            deleteCartPosition(currentProductId);

        }
    })

    
}

pageInit();