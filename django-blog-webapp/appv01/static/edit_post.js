document.addEventListener('click', function(e) {
    if (e.target.classList.contains('delete-btn')) {
        e.preventDefault();
        
        if (confirm("Permanently delete this post?")) {
            const url = e.target.getAttribute('data-url');
            const card = e.target.closest('.blog-card');

            fetch(url, {
                method: 'GET',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.9)';
                    card.style.transition = '0.3s ease';
                    setTimeout(() => card.remove(), 300);
                }
            });
        }
    }
});