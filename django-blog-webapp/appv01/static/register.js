function getCookie(name) {
    if (!document.cookie) return null;
    const xsrfCookies = document.cookie.split(';')
        .map(c => c.trim())
        .filter(c => c.startsWith(name + '='));
    if (xsrfCookies.length === 0) return null;
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}

document.getElementById('registrationForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');

    const userData = {
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
    };

    submitBtn.disabled = true;
    submitBtn.innerText = "Processing...";

    try {
        const response = await fetch('/registration/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(userData)
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = "/login/?signup=success";
        } else {
            const errorMessage = result.message || "Registration failed. Please try again.";
            
            alert(errorMessage); 
            
            submitBtn.disabled = false;
            submitBtn.innerText = "Create Account";
        }
    } catch (err) {
        console.error("Network Error:", err);
        alert("Server connection failed. Please try again.");
        submitBtn.disabled = false;
        submitBtn.innerText = "Create Account";
    }
});