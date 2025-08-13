// Django Chat WebSocket Implementation
class DjangoChat {
    constructor(orderId, userId, isAdmin = false) {
        this.orderId = orderId;
        this.userId = userId;
        this.isAdmin = isAdmin;
        this.socket = null;
        this.typingTimer = null;
        this.typingTimeout = 3000;
        this.isTyping = false;
        
        this.init();
    }
    
    init() {
        // WebSocket connection
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const socketUrl = `${protocol}//${window.location.host}/ws/chat/${this.orderId}/`;
        
        this.socket = new WebSocket(socketUrl);
        
        this.socket.onopen = () => {
            console.log('Chat connected');
            this.showStatus('Connected to chat');
        };
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.socket.onclose = () => {
            console.log('Chat disconnected');
            this.showStatus('Disconnected from chat');
        };
        
        this.socket.onerror = (error) => {
            console.error('Chat error:', error);
            this.showStatus('Connection error');
        };
        
        // Bind form events
        this.bindEvents();
    }
    
    bindEvents() {
        const form = document.getElementById('chat-form');
        const input = document.getElementById('chat-input');
        
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }
        
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                } else {
                    this.handleTyping();
                }
            });
            
            input.addEventListener('input', () => {
                this.handleTyping();
            });
        }
    }
    
    sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (message && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                'type': 'message',
                'message': message,
                'user_id': this.userId,
                'is_admin': this.isAdmin
            }));
            
            input.value = '';
            this.stopTyping();
        }
    }
    
    handleMessage(data) {
        if (data.type === 'message') {
            this.displayMessage({
                message: data.message,
                user_name: data.user_name,
                is_admin: data.is_admin,
                timestamp: data.timestamp
            });
        } else if (data.type === 'typing') {
            this.displayTyping(data.user_name, data.is_typing);
        }
    }
    
    displayMessage(data) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${data.is_admin ? 'admin-message' : 'user-message'}`;
        
        const timestamp = new Date(data.timestamp).toLocaleTimeString();
        
        messageDiv.innerHTML = `
            <div class="message-header">
                <strong>${data.user_name}</strong>
                <span class="message-time">${timestamp}</span>
            </div>
            <div class="message-content">${this.escapeHtml(data.message)}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    handleTyping() {
        if (!this.isTyping) {
            this.isTyping = true;
            this.socket.send(JSON.stringify({
                'type': 'typing',
                'user_id': this.userId,
                'is_typing': true
            }));
        }
        
        clearTimeout(this.typingTimer);
        this.typingTimer = setTimeout(() => {
            this.stopTyping();
        }, this.typingTimeout);
    }
    
    stopTyping() {
        if (this.isTyping) {
            this.isTyping = false;
            this.socket.send(JSON.stringify({
                'type': 'typing',
                'user_id': this.userId,
                'is_typing': false
            }));
        }
        clearTimeout(this.typingTimer);
    }
    
    displayTyping(userName, isTyping) {
        const typingDiv = document.getElementById('typing-indicator');
        if (!typingDiv) return;
        
        if (isTyping) {
            typingDiv.innerHTML = `<em>${userName} is typing...</em>`;
            typingDiv.style.display = 'block';
        } else {
            typingDiv.style.display = 'none';
        }
    }
    
    showStatus(message) {
        const statusDiv = document.getElementById('chat-status');
        if (statusDiv) {
            statusDiv.textContent = message;
            statusDiv.style.display = 'block';
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 3000);
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    close() {
        if (this.socket) {
            this.socket.close();
        }
        clearTimeout(this.typingTimer);
    }
}

// Global chat instance
let chatInstance = null;

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        const orderId = chatContainer.dataset.orderId;
        const userId = chatContainer.dataset.userId;
        const isAdmin = chatContainer.dataset.isAdmin === 'true';
        
        if (orderId && userId) {
            chatInstance = new DjangoChat(orderId, userId, isAdmin);
        }
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (chatInstance) {
        chatInstance.close();
    }
});