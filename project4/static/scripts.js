document.getElementById('converter-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    fetch('/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.converted_amount !== undefined) {
            document.getElementById('result').textContent = `Converted Amount: ${data.converted_amount}`;
            // Fetch and display conversion history
            fetch('/history')
                .then(response => response.json())
                .then(historyData => {
                    const historyList = document.createElement('ul');
                    historyData.forEach(entry => {
                        const listItem = document.createElement('li');
                        listItem.textContent = `${entry.amount} ${entry.from_currency} = ${entry.converted_amount} ${entry.to_currency}`;
                        historyList.appendChild(listItem);
                    });
                    document.getElementById('history').innerHTML = '<h2>Conversion History</h2>';
                    document.getElementById('history').appendChild(historyList);
                });
        } else {
            document.getElementById('result').textContent = 'Unsupported conversion.';
        }
    });
});
