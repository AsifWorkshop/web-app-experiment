document.addEventListener('DOMContentLoaded', function() {
    function refreshCommentCounts() {
        const countSpans = document.querySelectorAll('.comment-count');
        
        countSpans.forEach(span => {
            const postId = span.getAttribute('data-post-id');
            
            fetch(`/get-comment-count/${postId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        span.innerText = data.total_count;
                    }
                })
                .catch(err => console.error("Could not update count:", err));
        });
    }

    refreshCommentCounts();
    
    setInterval(refreshCommentCounts, 30000);
});