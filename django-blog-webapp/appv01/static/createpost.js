document.getElementById('postForm').addEventListener('submit', async (e) => {
    e.preventDefault()

    const formdata = new FormData()
    formdata.append('title', document.getElementById('title').value)
    formdata.append('content', document.getElementById('content').value)
    formdata.append('tags', document.getElementById('tags').value)
    const ImageInput = document.getElementById('post-image')

    if (ImageInput.files.length > 0) {
        formdata.append('attachment', ImageInput.files[0])
    }

    //Debug check ----

    for (let [key, value] of formdata.entries()) {
        console.log(key, value);
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    try {
        const response = await fetch('/create-post/', {
            method: 'POST',
            body: formdata,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        if (response.ok) {
            const result = await response.json()
            console.log('Post created:', result)
            window.location.href = '/'
        } else {
            console.error('Server error')
        }
    }
    catch (err) {
        console.error('Network error:', err)
    }
})