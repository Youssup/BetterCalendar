document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loginButton').addEventListener('click', function() {
        fetch('http://127.0.0.1:5000/login')
            .then(response => response.json())
            .then(data => {
                alert(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('runButton').addEventListener('click', function() {
        fetch('http://127.0.0.1:5000/run')
            .then(response => response.json())
            .then(data => {
                alert(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});