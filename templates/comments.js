document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submit_comment').addEventListener('click', function () {
        const commentInput = document.getElementById('comment_input').value;

        if (commentInput.trim()) {
            fetch('/add_comment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ comment: commentInput })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('comment_input').value = ''; // Clear input field
                    loadComments(); // Reload comments
                } else {
                    alert('Error adding comment');
                }
            });
        } else {
            alert('Comment cannot be empty');
        }
    });

    document.getElementById('load_comments').addEventListener('click', function () {
        loadComments();
    });

    function loadComments() {
        fetch('/get_comments')
            .then(response => response.json())
            .then(data => {
                const commentsList = document.getElementById('comments_list');
                commentsList.innerHTML = ''; // Clear previous comments

                data.comments.forEach(comment => {
                    const commentDiv = document.createElement('div');
                    commentDiv.classList.add('comment');
                    commentDiv.textContent = comment;
                    commentsList.appendChild(commentDiv);
                });
            });
    }
});
