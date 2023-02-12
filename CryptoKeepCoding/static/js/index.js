const currencies = ["EUR", "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT",	"MATIC"];

const onload = () => {
    fillCurrencies();
    fetchMovements();
    fetchStatus()
}

const fetchMovements = () => {
    fetch('http://127.0.0.1:5000/api/v1/movimientos')
    .then((response) => response.json())
    .then((data) => {
        if (data["status"] == "fail") {
            showAlertError(data["mensaje"])
        } else {
            fillTable(data["data"])
        }
    })
    .catch(error => showAlertError("Error 404") );
}

const fetchStatus = () => {
    fetch('http://127.0.0.1:5000/api/v1/status')
    .then((response) => response.json())
    .then((data) => {
        if (data["status"] == "fail") {
            showAlertError(data["mensaje"])
        } else {
            fillStatus(data["data"])
        }
    })
    .catch(error => showAlertError("Error 404") );
}

const fillTable = (movements) => {
    const table = document.querySelector("#movements");
    movements.forEach(movement => {
        const row = document.createElement('tr');
        row.appendChild(rowNodeItem(movement['fecha']));
        row.appendChild(rowNodeItem(movement['hora']));
        row.appendChild(rowNodeItem(movement['from_moneda']));
        row.appendChild(rowNodeItem(movement['from_cantidad']));
        row.appendChild(rowNodeItem(movement['to_moneda']));
        row.appendChild(rowNodeItem(movement['to_cantidad']));
        table.appendChild(row);
    });
}

const rowNodeItem = (movement) => {
    const node = document.createElement('td');
    const text = document.createTextNode(movement);
    node.appendChild(text);
    return node

}

const fillStatus = (data) => {
    const table = document.querySelector("#status");
    table.removeAttribute("hidden"); 
    document.querySelector("#invested").innerHTML = data["invested"];
    document.querySelector("#recovered").innerHTML = data["recovered"];
    document.querySelector("#purchase-value").innerHTML =data["purchase_value"];
    document.querySelector("#current-value").innerHTML = data["current_value"];
}

const fillCurrencies = () => {
    const fromCurrencySelect = document.querySelector("#from_currency");
    
    currencies.forEach(currency => { 
        const option = document.createElement("option");
        option.value = currency;
        option.innerHTML = currency;
        fromCurrencySelect.appendChild(option);
    })
    const toCurrencySelect = document.querySelector("#to_currency");
    currencies.forEach(currency => { 
        const option = document.createElement("option");
        option.value = currency;
        option.innerHTML = currency;
        toCurrencySelect.appendChild(option);
    })
}

const calculateConversion = () => {
    const fromCurrencySelect = document.querySelector("#from_currency").value
    const fromValue = document.querySelector("#q-from").value;
    const toCurrencySelect = document.querySelector("#to_currency").value
    if (fromValue == "" || fromCurrencySelect == "" || fromValue == 0) { return }
    if (toCurrencySelect == "" || fromCurrencySelect == toCurrencySelect) { return }
    fetch(`http://127.0.0.1:5000/api/v1/tasa/${fromCurrencySelect}/${toCurrencySelect}`)
    .then((response) => response.json())
    .then((data) => {
        if (data["status"] == "fail") {
            showAlertError(data["mensaje"])
        } else {
            document.querySelector("#q-to").value = fromValue * data["rate"];
            document.querySelector("#pu").value = data["rate"];
            enablePurchaseButton()
        }
    })
    .catch(error => showAlertError("Error 404") );
}

const makePurchase = () => {
   const dateTime = new Date();
   const fecha = dateTime.toISOString().split('T')[0];
   const hora = dateTime.toISOString().split('T')[1];
   const from_moneda = document.querySelector("#from_currency").value;
   const from_cantidad = document.querySelector("#q-from").value;;
   const to_moneda = document.querySelector("#to_currency").value;
   const to_cantidad = document.querySelector("#q-to").value;
   postPurchase(fecha, hora, from_moneda, from_cantidad, to_moneda, to_cantidad)
}

const postPurchase = (fecha, hora, from_moneda, from_cantidad, to_moneda, to_cantidad) => {
    fetch('http://127.0.0.1:5000/api/v1/movimiento', {
        method: 'POST',
        body: JSON.stringify({
            fecha:fecha,
            hora:hora,
            from_moneda:from_moneda,
            from_cantidad:from_cantidad,
            to_moneda:to_moneda,
            to_cantidad:to_cantidad}),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        }
    })
    .then((response) => response.json())
    .then((data) => {
        if (data["status"] == "fail") {
            showAlertError(data["mensaje"])
        } else {
            reload()
        }
    })
    .catch(error => showAlertError("Error 404") );
}

const showPurchase = () => {
    const purchaseContainer = document.querySelector("#purchase");
    if (purchaseContainer.hasAttribute("hidden")) {
        purchaseContainer.removeAttribute("hidden"); 
    }
}

const disablePurchaseButton = () => {
    const purchaseButton = document.querySelector("#purchase-button");
    if (!purchaseButton.hasAttribute("disabled")) {
        purchaseButton.setAttribute("disabled", "");
    }
}

const enablePurchaseButton = () => {
    const purchaseButton = document.querySelector("#purchase-button");
    if (purchaseButton.hasAttribute("disabled")) {
        purchaseButton.removeAttribute("disabled");
    }
}

const showAlertError = (error) => {
    alert(error);
}

const reload = () => {
    location.reload();
}