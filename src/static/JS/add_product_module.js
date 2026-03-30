export class AddProductWindow {
    constructor() {
        this.addingWindowElement = document.getElementById("adding-window-bg");
        this.addingBtnElement = document.getElementById("addingProductButton");

        this.incCountProductBrnElement = document.getElementById("incrementAddingWindowВtn");
        this.decCountProductBrnElement = document.getElementById("decrementAddingWindowВtn");
        this.productImageelement = document.getElementById("add-window-product-image");
        this.productNameElement = document.getElementById("add-window-product-name");
        this.productCountPElement = document.getElementById("productCountLabel");
        this.productPricePElement = document.getElementById("productPriceLabel");


        this.productInfo = {
            "productId": null,
            "productPrice": null,
            "productCount": null
        };


        this.addingWindowElement.addEventListener('click', (event) => {
            if (event.target === this.addingWindowElement) {
                this.addingWindowElement.style.display = "none"
                this.productInfo = {
                    "productId": null,
                    "productPrice": null,
                    "productCount": null
                };
            }
        });

        this.incCountProductBrnElement.addEventListener('click', () => {
            this.productInfo.productCount ++;
            this.productCountPElement.textContent = this.productInfo.productCount;
            this.productPricePElement.textContent = `${(this.productInfo.productCount * this.productInfo.productPrice).toFixed(2)} р`;

        
        });

        this.decCountProductBrnElement.addEventListener('click', () => {
            if (this.productInfo.productCount > 1) {
                this.productInfo.productCount --;
                this.productCountPElement.textContent = this.productInfo.productCount;
                this.productPricePElement.textContent = `${(this.productInfo.productCount * this.productInfo.productPrice).toFixed(2)} р`;
            }
        });

        this.addingBtnElement.addEventListener('click', (event) => {
            event.stopPropagation();
            const productCart = JSON.parse(sessionStorage.getItem('productCart'));

            if (productCart.hasOwnProperty(this.productInfo.productId)) {
                productCart[this.productInfo.productId].count += this.productInfo.productCount; 
            } else {
                productCart[this.productInfo.productId] = {
                    "count": this.productInfo.productCount
                }
            }

            sessionStorage.setItem("productCart", JSON.stringify(productCart));

    
            this.productInfo = {
                "productId": null,
                "productPrice": null,
                "productCount": null
            };
            this.addingWindowElement.style.display = "none"
        });
    }

    openWindow(productId) {
        const productInfoObj = JSON.parse(sessionStorage.getItem("productInfo"))[productId];


        this.addingWindowElement.style.display = "flex";

        this.productInfo.productId = productId;
        this.productInfo.productPrice = productInfoObj.sale_price;
        this.productInfo.productCount = 1;

        this.productNameElement.textContent = productInfoObj.name;
        this.productImageelement.src = productInfoObj.image_irl;
        this.productCountPElement.textContent = "1";
        this.productPricePElement.textContent = `${(this.productInfo.productPrice).toFixed(2)} р`;
    }
}




