function fetchBookSuggestions() {
    const query = document.getElementById('book_title').value;

    if (query.length > 0) {
        fetch(`/get_book_suggestions?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                let suggestionsBox = document.getElementById('book_suggestions');
                suggestionsBox.innerHTML = ''; // Clear previous suggestions

                data.forEach(book => {
                    let suggestion = document.createElement('div');
                    suggestion.classList.add('suggestion-item');
                    suggestion.textContent = book;
                    suggestion.onclick = () => {
                        document.getElementById('book_title').value = book;
                        suggestionsBox.innerHTML = ''; // Clear suggestions after selection
                    };
                    suggestionsBox.appendChild(suggestion);
                });
            })
            .catch(error => {
                console.error('Error fetching book suggestions:', error);
            });
    } else {
        document.getElementById('book_suggestions').innerHTML = ''; // Clear suggestions if input is empty
    }
}
