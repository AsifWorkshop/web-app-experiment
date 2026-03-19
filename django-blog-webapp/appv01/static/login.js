function getCookie(name) {
    if (!document.cookie) return null;
    const xsrfCookies = document.cookie.split(';')
        .map(c => c.trim())
        .filter(c => c.startsWith(name + '='));
    if (xsrfCookies.length === 0) return null;
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}


document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    submitBtn.disabled = true;
    submitBtn.innerText = "Authenticating...";

    try {
        const response = await fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();

        if (response.ok) {
            // Success! Redirect to home or dashboard
            window.location.href = "/"; 
        } else {
            alert(result.message || "Invalid credentials");
            submitBtn.disabled = false;
            submitBtn.innerText = "Sign In";
        }
    } catch (err) {
        console.error("Login Error:", err);
        alert("Connection failed.");
        submitBtn.disabled = false;
        submitBtn.innerText = "Sign In";
    }
});