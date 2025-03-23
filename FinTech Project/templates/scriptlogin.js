document.getElementById('investor-listener-info-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    const response = await fetch('/investor-listener-information', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (response.ok) {
        alert(result.message);
        // Redirect to another page (e.g., dashboard)
        window.location.href = '/dashboard';
    } else {
        alert(result.error);
    }
});