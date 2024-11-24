document.getElementById('search-btn').addEventListener('click', function(e) {
    e.preventDefault();
    const query = document.getElementById('search-input').value.trim();
    fetch(`/search_query?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('search-results');
            resultsDiv.innerHTML = ''; // Очистити попередні результати
            if (data.results.length > 0) {
                data.results.forEach(game => {
                    const gameDiv = document.createElement('div');
                    gameDiv.innerHTML = `
                        <h3>${game.name}</h3>
                        <p><strong>Description:</strong> ${game.description}</p>
                    `;
                    resultsDiv.appendChild(gameDiv);
                });
            } else {
                resultsDiv.innerHTML = '<p>No games found.</p>';
            }
        });
});
