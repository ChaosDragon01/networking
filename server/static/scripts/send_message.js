function fetchMessages() {
    fetch('/get_messages')
        .then(response => response.json())
        .then(data => {
            const messagesDiv = document.querySelector('.messages');
            messagesDiv.innerHTML = '';
            data.messages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message';
                messageDiv.innerHTML = `<strong>${msg.username}:</strong> ${msg.message}`;
                messagesDiv.appendChild(messageDiv);
            });
        });
}

setInterval(fetchMessages, 5000); // Refresh messages every 5 seconds
window.onload = fetchMessages; // Fetch messages on page load