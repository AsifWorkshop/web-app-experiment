function toggleReplyForm(commentId) {
        const form = document.getElementById(`reply-form-${commentId}`);
        if (form.classList.contains('d-none')) {
            form.classList.remove('d-none');
        } else {
            form.classList.add('d-none');
        }
    }