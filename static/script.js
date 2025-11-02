// Chat application JavaScript
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const chatMessages = document.getElementById('chatMessages');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');

// Store conversation history
let conversationHistory = [];

// Format timestamp
function getTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

// Add message to chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    // Check for image URLs in the format [IMAGE:url]
    const imageRegex = /\[IMAGE:(.*?)\]/g;
    let processedContent = content;
    const images = [];

    // Extract images
    let match;
    while ((match = imageRegex.exec(content)) !== null) {
        images.push(match[1]);
        processedContent = processedContent.replace(match[0], '');
    }

    // Add images first
    images.forEach(imageUrl => {
        const img = document.createElement('img');
        img.src = imageUrl;
        img.alt = 'Car image';
        img.className = 'car-image';
        messageContent.appendChild(img);
    });

    // Split content into paragraphs
    const paragraphs = processedContent.split('\n').filter(p => p.trim());
    paragraphs.forEach(paragraph => {
        const p = document.createElement('p');
        p.textContent = paragraph;
        messageContent.appendChild(p);
    });

    const timestamp = document.createElement('span');
    timestamp.className = 'timestamp';
    timestamp.textContent = getTimestamp();
    messageContent.appendChild(timestamp);

    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    scrollToBottom();

    // Update conversation history
    conversationHistory.push({
        role: isUser ? 'user' : 'assistant',
        content: content
    });
}

// Show typing indicator
function showTyping() {
    typingIndicator.style.display = 'block';
    scrollToBottom();
}

// Hide typing indicator
function hideTyping() {
    typingIndicator.style.display = 'none';
}

// Scroll to bottom of chat
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Send message to backend
async function sendMessage(message) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        if (data.success) {
            return data.response;
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    } catch (error) {
        console.error('Error:', error);
        return "I apologize, but I'm having trouble connecting right now. Please try again in a moment.";
    }
}

// Handle form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = messageInput.value.trim();
    if (!message) return;

    // Disable input while processing
    messageInput.disabled = true;
    sendButton.disabled = true;

    // Add user message
    addMessage(message, true);

    // Clear input
    messageInput.value = '';

    // Show typing indicator
    showTyping();

    // Get bot response
    const botResponse = await sendMessage(message);

    // Hide typing indicator
    hideTyping();

    // Add bot response
    addMessage(botResponse, false);

    // Re-enable input
    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.focus();
});

// Auto-focus input on load
window.addEventListener('load', () => {
    messageInput.focus();
    scrollToBottom();
});

// Handle enter key (without shift for send)
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// Keep input focused
chatMessages.addEventListener('click', () => {
    messageInput.focus();
});
