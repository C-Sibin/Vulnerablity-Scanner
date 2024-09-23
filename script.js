document.getElementById('scanButton').addEventListener('click', function() {
    const loading = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const downloadLink = document.getElementById('downloadLink');

    loading.style.display = 'block';
    resultDiv.style.display = 'none';
    downloadLink.style.display = 'none';

    fetch('/scan', {
        method: 'POST'
    }).then(response => response.json())
    .then(data => {
        loading.style.display = 'none';
        resultDiv.style.display = 'block';

        let resultHtml = `<h2>Scan Results:</h2><pre>`;

        for (const [section, content] of Object.entries(data.system_info)) {
            resultHtml += `<strong>${section}</strong>:<br>${content}<br><br>`;
        }

        for (const [section, content] of Object.entries(data.network_info)) {
            resultHtml += `<strong>${section}</strong>:<br>${content}<br><br>`;
        }

        resultHtml += `</pre>`;
        resultDiv.innerHTML = resultHtml;

        downloadLink.href = data.download_link;
        downloadLink.style.display = 'block';
    }).catch(err => {
        loading.style.display = 'none';
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `<p>Error: ${err.message}</p>`;
    });
});
