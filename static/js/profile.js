document.getElementById('edit-profile-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/api/update-profile', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Profile updated successfully!');
        } else {
            alert('There was an error updating your profile.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error updating your profile.');
    });
});
