console.log("searchh")

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('navSearchInput');
    const noResultsMsg = document.getElementById('search-no-results');
    let typingTimer;
    const doneTypingInterval = 1000; 

    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function performSearch() {
        const query = searchInput.value.trim();
        const postWrappers = document.querySelectorAll('.post-wrapper');

        
        if (query === "") {
            postWrappers.forEach(w => w.style.display = 'block');
            if (noResultsMsg) noResultsMsg.style.display = 'none';
            return;
        }

        fetch('/search-posts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 'q': query })
        })
        .then(res => res.json())
        .then(data => {
            const ids = data.matching_ids;
            let foundAny = false;

            postWrappers.forEach(wrapper => {
                const currentId = parseInt(wrapper.getAttribute('data-post-id'));
                if (ids.includes(currentId)) {
                    wrapper.style.display = 'block';
                    foundAny = true;
                } else {
                    wrapper.style.display = 'none';
                }
            });

            if (noResultsMsg) {
                noResultsMsg.style.display = foundAny ? 'none' : 'block';
            }
        })
        .catch(err => console.error("Search Error:", err));
    }

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(performSearch, doneTypingInterval);
        });

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                clearTimeout(typingTimer);
                performSearch();
            }
        });
    }
});