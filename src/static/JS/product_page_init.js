import { loadProducts } from "./server_queries.js";

async function initPage() {
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
        console.log(newProductInfoObject);
        sessionStorage.setItem('productInfo', JSON.stringify(newProductInfoObject));
    }

}

initPage();