let isProcessing = false;

document.addEventListener('click', function(e) {
    const btn = e.target.closest('.like-button');
    if (!btn || isProcessing) return;

    e.preventDefault();
    e.stopImmediatePropagation(); 
    
    isProcessing = true; 
    
    const postId = btn.getAttribute('data-post-id');
    const countSpan = btn.querySelector('.likes-count-text');
    const heartPath = btn.querySelector('.like-heart-path');
    const csrftoken = btn.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/like/${postId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            countSpan.innerText = data.new_count;
            
        
            if (data.is_liked) {
                heartPath.setAttribute('fill', '#ed4956');
                heartPath.setAttribute('stroke', '#ed4956');
            } else {
                heartPath.setAttribute('fill', 'none');
                heartPath.setAttribute('stroke', 'currentColor');
            }
        }
    })
    .finally(() => {
        isProcessing = false; 
    });
});