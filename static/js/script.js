document.getElementById('playlist-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const playlistUrl = document.getElementById('playlist-url').value;
    
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: playlistUrl })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerText = 'Error: ' + data.error;
        } else {
            document.getElementById('result').innerText = 'Total Duration: ' + data.total_duration;
        }
    })
    .catch(error => {
        document.getElementById('result').innerText = 'Error: ' + error.message;
    });
});
