function pageInit() {
    const addingWindowElement = document.getElementById("adding-window-bg");
    const addingBtnElement = document.getElementById("addingProductButton");

    const incCountProductBrnElement = document.getElementById("incrementAddingWindowВtn");
    const decCountProductBrnElement = document.getElementById("decrementAddingWindowВtn");
    const productImageelement = document.getElementById("add-window-product-image");
    const productNameElement = document.getElementById("add-window-product-name");

    const productCountPElement = document.getElementById("productCountLabel");
    const productPricePElement = document.getElementById("productPriceLabel");


    const lastSeengProductInfo = {
        "productId": null,
        "productPrice": null,
        "productCount": null
    };

    document.addEventListener('click', (event) => {
        if (event.target === addingWindowElement) {
            addingWindowElement.style.display = "none"
            lastSeengProductInfo.productId = null;
            lastSeengProductInfo.productPrice = null;
            lastSeengProductInfo.productCount = null;

        } else if (event.target.classList.contains("in-cart-button")) {
            event.stopImmediatePropagation();
            const currentProductId = event.target.getAttribute("productid") || event.target.productid;
            console.log(currentProductId);
            const productInfoObj = JSON.parse(sessionStorage.getItem("productInfo"))[currentProductId];

            addingWindowElement.style.display = "flex";
            lastSeengProductInfo.productId = currentProductId;
            productNameElement.textContent = productInfoObj.name;
            lastSeengProductInfo.productPrice = productInfoObj.sale_price;
            productImageelement.src = productInfoObj.image_irl;
            lastSeengProductInfo.productCount = 1;

            productCountPElement.textContent = lastSeengProductInfo.productCount;
            productPricePElement.textContent = `${(lastSeengProductInfo.productCount * lastSeengProductInfo.productPrice).toFixed(2)} р`;
        } 
    });



    incCountProductBrnElement.addEventListener('click', () => {
        lastSeengProductInfo.productCount ++;
        productCountPElement.textContent = lastSeengProductInfo.productCount;
        productPricePElement.textContent = `${(lastSeengProductInfo.productCount * lastSeengProductInfo.productPrice).toFixed(2)} р`;
    });

    decCountProductBrnElement.addEventListener('click', () => {
        if (lastSeengProductInfo.productCount > 1) {
            lastSeengProductInfo.productCount --;
            productCountPElement.textContent = lastSeengProductInfo.productCount;
            productPricePElement.textContent = `${(lastSeengProductInfo.productCount * lastSeengProductInfo.productPrice).toFixed(2)} р`;
        }
    });


    addingBtnElement.addEventListener('click', (event) => {
        event.stopPropagation();
        const productCart = JSON.parse(sessionStorage.getItem('productCart'));

        if (productCart.hasOwnProperty(lastSeengProductInfo.productId)) {
            productCart[lastSeengProductInfo.productId].count += lastSeengProductInfo.productCount; 
        } else {
            productCart[lastSeengProductInfo.productId] = {
                "count": lastSeengProductInfo.productCount
            }
        }

        sessionStorage.setItem("productCart", JSON.stringify(productCart));

    
        lastSeengProductInfo.productId = null;
        lastSeengProductInfo.productPrice = null;
        lastSeengProductInfo.productCount = null;
        addingWindowElement.style.display = "none"
    });
}

pageInit()


