export class LikedProductCirtain {
    constructor() {
        this.cirtainWindowElement = document.getElementById('black-liked-products-bg');
        this.cirtainProductContainerElement = document.getElementById('liked-products-block');
        this.closeCirtainButtonElement = document.getElementById("close-liked-button");
     
        this.closeCirtainButtonElement.addEventListener('click', () => {
            this.closeProductCirtain();
        })

    

        document.addEventListener('click', (event) => {
            if (event.target === this.cirtainWindowElement) {
                this.closeProductCirtain();
            }
        });
    }

    closeProductCirtain() {
        this.cirtainWindowElement.style.display = 'none';
        this.cirtainProductContainerElement.replaceChildren();
    }


    openWindow() {
        this.cirtainWindowElement.style.display = "flex";

        const likedProductsData = JSON.parse(localStorage.getItem('likedProducts'));
        const productInfoData = JSON.parse(sessionStorage.getItem('productInfo'));
        const productBlock = document.createDocumentFragment();

        for(const productId of likedProductsData) {

            const productInfoObj = productInfoData[productId];
            if (!productInfoObj) {
                continue
            }
           
            const newProductElement = document.createElement('div');
            newProductElement.classList.add('product-in-cart');
            newProductElement.id = `product-liked-position-${productId}`;

            const productImageElement = document.createElement('img');
            productImageElement.src = productInfoObj.image_irl;
            newProductElement.append(productImageElement);

            const productInfoElement = document.createElement('div');
            productInfoElement.classList.add('product-in-cart-info');

            const productNamePElement = document.createElement('p');
            productNamePElement.classList.add('product-name');
            productNamePElement.textContent = productInfoObj.name;
            productInfoElement.append(productNamePElement);

            const productWeightPElement = document.createElement('p');
            productWeightPElement.classList.add('product-weight');
            productWeightPElement.textContent = `${productInfoObj.weight} г`;
            productInfoElement.append(productWeightPElement);

            const productPricePElement = document.createElement('p');
            productPricePElement.classList.add('product-price');
            productPricePElement.textContent = `${productInfoObj.sale_price} р`;
            productInfoElement.append(productPricePElement);

            newProductElement.append(productInfoElement);


            const productControlButtonsElement = document.createElement('div');
            productControlButtonsElement.classList.add('liked-products-change-buttons');

            const likeProductButton = document.createElement('button');
            likeProductButton.style.backgroundImage = 'url(/static/StaticImages/active_liked_image.png)';
            likeProductButton.setAttribute('productId', productId);
            likeProductButton.setAttribute('data-js-liked-button', '')
            productControlButtonsElement.append(likeProductButton);


            const inCartProductButton = document.createElement('button');
            inCartProductButton.classList.add('add-position-button');
            inCartProductButton.setAttribute('productId', productId);
            inCartProductButton.setAttribute('data-js-in-cart-button', '');
            productControlButtonsElement.append(inCartProductButton);
            
            newProductElement.append(productControlButtonsElement);

            productBlock.append(newProductElement);



        }
        this.cirtainProductContainerElement.append(productBlock);
    }

    setLikedPosition(eventTargetButton, productId) {
        let likedProducts = JSON.parse(localStorage.getItem('likedProducts'));
        if (!likedProducts.includes(productId)) {
            eventTargetButton.style.backgroundImage = 'url(/static/StaticImages/active_liked_image.png)';
            likedProducts.push(productId);
        } else {
            eventTargetButton.style.backgroundImage = 'url(/static/StaticImages/liked_button_image.png)';
            likedProducts = likedProducts.filter(prodId => prodId != productId)
        }
        localStorage.setItem('likedProducts', JSON.stringify(likedProducts));
    }
}


    