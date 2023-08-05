function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function base(serviceId) {
    try {
        await fetch(`/services/update_is_read/${serviceId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ is_read: true }),
        });
    } catch (error) {
        console.error('Error updating is_read:', error);
    }
}

async function handleClick(event) {
    event.preventDefault();
    const serviceId = event.currentTarget.dataset.serviceId;
    await base(serviceId);
    window.location.href = document.querySelector('a#unread_msg').getAttribute('href');
}