export async function loadProducts() {
    const productsPromise = await fetch(`${window.location.origin}/sitedata/product`);
    const products = await productsPromise.json();
    return products
}

export async function resfreshAccessToken() {
    const result = await fetch(
        `${window.location.origin}/site/login/refresh`, 
        {
            method: "POST",
            headers: {'Content-Type': 'application/json'}
        }
    );
    if (result.status === 200) {
        const json_result = await result.json();
        localStorage.setItem(json_result.token_type, json_result.access_token);
        return true;
    }
    return false;

}

export async function createOrder(username, phone, productArray, selectedBranchId, commentStr, fullOrderDateStr, recAttemp=0) {
    if (recAttemp > 3) return "ToManyAttemp";
    
    const accessToken = localStorage.getItem("bearer");
    try {
        const result = await fetch(
            `${window.location.origin}/sitedata/orders/add`, 
            {
                method: "POST",
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "username": username,
                    "phone": phone,
                    "items": productArray,
                    "order_datetime": fullOrderDateStr,
                    "branch_id": selectedBranchId,
                    "comment": commentStr
                })
            }
        )

        switch (result.status) {
            case 403: {
                localStorage.removeItem('bearer');
                for(const i = 1; i < 4; i++) {
                    if (await resfreshAccessToken()) break;
                }
                if (localStorage.getItem("bearer")) {
                    return createOrder(username, phone, productArray, selectedBranchId, commentStr, fullOrderDateStr, recAttemp+1);
                } else {
                    return "AuthError"
                }
                break;
            }
            case 422: {                
                const jsonResult = await result.json();

                if (jsonResult.message === "UncorrectBranch" || jsonResult.message === "UnavaliableBranch") {
                    return "UncorrectBranch"
                }

                if (jsonResult.message === "UnavaliableProduct") {
                    const productCart = JSON.parse(sessionStorage.getItem('productCart'));
                    for (const productId of jsonResult.products) {
                        delete productCart[productId]
                    }
                    sessionStorage.setItem('productCart', JSON.stringify(productCart));

                    return "UnavaliableProduct"
                }
                break;
            }
            default: return "Created";
        }
    } catch (error) {
        return "NetWorkError";
    }
}

export async function sendSupportMail(userName, userEmail, mailTheme, mailText) {
    try {
        const rawResult = await fetch(
            `${window.location.origin}/sitedata/support`,
            {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "username": userName,
                    "user_email": userEmail,
                    "message_theme": mailTheme,
                    "message_text": mailText
                })
            }
        )
        const result = await rawResult.json();
        return result.message;

    } catch (error) {
        return "NetworkError";
    }
}
