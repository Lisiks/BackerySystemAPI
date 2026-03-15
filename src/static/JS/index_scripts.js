async function loadProducts() {
    const productsPromise = await fetch('http://127.0.0.1:8000/sitedata/product');
    const products = await productsPromise.json();


    products.categories.forEach(category => {
        const currentProductContainer = document.querySelector(`#category-${category.category_id} > .product-container`);
        const addingFragment = document.createDocumentFragment();

        category.products.forEach(product => {
            const newProductCardElement = document.createElement('div');
            newProductCardElement.classList.add('product-card');
            newProductCardElement.id = `product-${product.id}`;
            
            const imageElement = document.createElement('img');
            imageElement.src = product.image_url;
            newProductCardElement.append(imageElement);

            const productNameTextElement = document.createElement('p');
            productNameTextElement.textContent = `${product.name}`;
            newProductCardElement.append(productNameTextElement);


            const productInfoTextElement = document.createElement('p');

            const productInfoTextPriceElement = document.createElement('span');
            productInfoTextPriceElement.textContent = `${product.sale_price} р `;
            productInfoTextPriceElement.classList.add('product-price-span');
            productInfoTextElement.append(productInfoTextPriceElement);

            const productInfoTextWeightElement = document.createElement('span');
            productInfoTextWeightElement.textContent = `${product.weight} г`;
            productInfoTextWeightElement.classList.add('product-weight-span');
            productInfoTextElement.append(productInfoTextWeightElement);

            newProductCardElement.append(productInfoTextElement);

            const inCartButtonElement = document.createElement('button');
            inCartButtonElement.textContent = 'В корзину';
            inCartButtonElement.classList.add('in-cart-button');
            newProductCardElement.append(inCartButtonElement);

            addingFragment.append(newProductCardElement);
        })
        currentProductContainer.append(addingFragment);
    });
}

loadProducts()