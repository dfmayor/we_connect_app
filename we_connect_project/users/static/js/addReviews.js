function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function addReviews() {
    const rating = document.querySelector('select[name="rating"]').value;
    const comment = document.querySelector('textarea[name="comment"]').value;
    const service_id = document.getElementById("service_id").value;

    fetch('/services/add_review/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            service_id: service_id, rating: rating, comment: comment
        })
    })
    .then(response => response.json())
    .then(data => {
        const modal_body = document.getElementById("modal_body");
        const modalFooter = document.getElementById("modalFooter");
        modalFooter.innerHTML = '';
        const modalMessage = document.createElement('div');
        modal_body.innerHTML = '';
        if (data.status === 'success') {
            modalMessage.innerHTML = `
                <p>${data.message}</p>;
            `;
            modal_body.appendChild(modalMessage);
        } else {
            modalMessage.innerHTML = `
                <p>${data.message}</p>;
            `;
            modal_body.appendChild(modalMessage);
        }
    })
}