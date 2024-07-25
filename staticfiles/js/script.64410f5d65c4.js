function toggleSettings() {
    var settingsPanel = document.getElementById('settings-panel');
    if (settingsPanel.style.display === 'block') {
        settingsPanel.style.display = 'none';
    } else {
        settingsPanel.style.display = 'block';
    }
}

function showSection(sectionId) {
    var sections = document.querySelectorAll('.section');
    sections.forEach(function(section) {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

function sendMessage(event) {
    event.preventDefault();
    var messageInput = document.getElementById('chat-message');
    var chatBox = document.getElementById('chat-box');
    var message = messageInput.value;
    if (message.trim() === '') return;

    var userMessage = document.createElement('div');
    userMessage.className = 'chat-message user';
    userMessage.innerHTML = message;
    chatBox.appendChild(userMessage);
    
    // Simulate bot response
    setTimeout(function() {
        var botMessage = document.createElement('div');
        botMessage.className = 'chat-message bot';
        botMessage.innerHTML = 'This is a simulated response.';
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 1000);
    
    messageInput.value = '';
}

function broadcastMessage() {
    var message = document.getElementById('message').value;
    document.getElementById('broadcast-result').innerHTML = 'Broadcast message: ' + message;
}

function sendQueryToAI(event) {
    event.preventDefault();
    var queryInput = document.getElementById('query');
    var aiResponse = document.getElementById('ai-response');
    var query = queryInput.value;
    if (query.trim() === '') return;
    
    aiResponse.innerHTML = 'Processing your query: ' + query;
    queryInput.value = '';
}
