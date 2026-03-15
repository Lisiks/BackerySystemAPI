const shopingCartButtonElement = document.getElementById("shopping-cart-button");
const shopingCartMenuElement = document.getElementById("aside-block");

shopingCartButtonElement.addEventListener('click', () => {
    shopingCartMenuElement.classList.remove('hidden-block');
})

shopingCartMenuElement.addEventListener('click', (event) => {
    if (event.target === shopingCartMenuElement) {
       shopingCartMenuElement.classList.add("hidden-block"); 
    }
})