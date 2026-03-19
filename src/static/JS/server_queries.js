export async function loadProducts() {
    const productsPromise = await fetch(`${window.location.origin}/sitedata/product`);
    const products = await productsPromise.json();
    return products
}