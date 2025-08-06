// Professional Writers - Chat System

class ChatSystem {
    constructor() {
        this.socket = null;
        this.currentOrderId = null;
        this.isTyping = false;
        this.typingTimeout = null;
        this.init();
    }
    
    init() {
        // Initialize Socket.IO connection
        if (typeof io !== 'undefined') {
            this.socket = io();
            this.setupSocketListeners();
        }
        
        this.setupChatInterface();
        this.setupEventListeners();
    }
    
    setupSocketListeners() {
        this.socket.on('connect', () => {
            console.log('Connected to chat server');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from chat server');
        });
        
        this.socket.on('message', (data) => {
            this.displayMessage(data);
        });
        
        this.socket.on('typing', (data) => {
            this.showTypingIndicator(data);
        });
        
        this.socket.on('status', (data) => {
            this.showStatusMessage(data.msg);
        });
    }
    
    setupChatInterface() {
        const chatContainer = document.getElementById('chat-container');
        if (!chatContainer) return;
        
        // Get order ID from data attribute
        this.currentOrderId = chatContainer.dataset.orderId;
        
        if (this.currentOrderId && this.socket) {
            // Join the chat room for this order
            this.socket.emit('join', { order_id: this.currentOrderId });
            
            // Load existing messages
            this.loadChatHistory();
        }
    }
    
    setupEventListeners() {
        const chatForm = document.getElementById('chat-form');
        const chatInput = document.getElementById('chat-input');
        const chatMessages = document.getElementById('chat-messages');
        
        if (chatForm) {
            chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }
        
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
            
            chatInput.addEventListener('input', () => {
                this.handleTyping();
            });
        }
        
        // Auto-scroll to bottom when new messages arrive
        if (chatMessages) {
            const observer = new MutationObserver(() => {
                this.scrollToBottom();
            });
            observer.observe(chatMessages, { childList: true });
        }
    }
    
    sendMessage() {
        const chatInput = document.getElementById('chat-input');
        const message = chatInput.value.trim();
        
        if (!message || !this.socket || !this.currentOrderId) return;
        
        // Emit message to server
        this.socket.emit('message', {
            order_id: this.currentOrderId,
            message: message
        });
        
        // Clear input
        chatInput.value = '';
        
        // Stop typing indicator
        this.stopTyping();
    }
    
    displayMessage(data) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${data.is_admin ? 'admin' : 'user'}`;
        
        if (!data.is_admin && this.isCurrentUser(data.user_name)) {
            messageDiv.classList.add('own');
        }
        
        const timestamp = new Date(data.timestamp).toLocaleTimeString();
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <span class="message-sender">${data.user_name}</span>
                    <span class="message-time">${timestamp}</span>
                </div>
                <div class="message-text">${this.escapeHtml(data.message)}</div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    handleTyping() {
        if (!this.socket || !this.currentOrderId) return;
        
        if (!this.isTyping) {
            this.isTyping = true;
            this.socket.emit('typing', {
                order_id: this.currentOrderId,
                is_typing: true
            });
        }
        
        // Clear existing timeout
        clearTimeout(this.typingTimeout);
        
        // Set new timeout to stop typing indicator
        this.typingTimeout = setTimeout(() => {
            this.stopTyping();
        }, 2000);
    }
    
    stopTyping() {
        if (this.isTyping && this.socket && this.currentOrderId) {
            this.isTyping = false;
            this.socket.emit('typing', {
                order_id: this.currentOrderId,
                is_typing: false
            });
        }
    }
    
    showTypingIndicator(data) {
        const typingIndicator = document.getElementById('typing-indicator');
        if (!typingIndicator) return;
        
        if (data.is_typing && !this.isCurrentUser(data.user_name)) {
            typingIndicator.textContent = `${data.user_name} is typing...`;
            typingIndicator.style.display = 'block';
        } else {
            typingIndicator.style.display = 'none';
        }
    }
    
    showStatusMessage(message) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        
        const statusDiv = document.createElement('div');
        statusDiv.className = 'status-message';
        statusDiv.textContent = message;
        
        chatMessages.appendChild(statusDiv);
        this.scrollToBottom();
    }
    
    loadChatHistory() {
        if (!this.currentOrderId) return;
        
        fetch(`/api/chat/messages/${this.currentOrderId}`)
            .then(response => response.json())
            .then(messages => {
                const chatMessages = document.getElementById('chat-messages');
                if (chatMessages) {
                    chatMessages.innerHTML = '';
                    messages.forEach(message => {
                        this.displayMessage({
                            message: message.message,
                            user_name: message.user_name,
                            is_admin: message.is_admin,
                            timestamp: message.created_at
                        });
                    });
                }
            })
            .catch(error => {
                console.error('Error loading chat history:', error);
            });
    }
    
    scrollToBottom() {
        const chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    isCurrentUser(userName) {
        // This would be replaced with actual user identification logic
        const currentUserName = document.querySelector('[data-current-user]')?.dataset.currentUser;
        return userName === currentUserName;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Public methods for external use
    openChat(orderId) {
        this.currentOrderId = orderId;
        if (this.socket) {
            this.socket.emit('join', { order_id: orderId });
            this.loadChatHistory();
        }
        
        // Show chat modal or interface
        const chatModal = document.getElementById('chat-modal');
        if (chatModal && typeof bootstrap !== 'undefined') {
            const modal = new bootstrap.Modal(chatModal);
            modal.show();
        }
    }
    
    closeChat() {
        if (this.socket && this.currentOrderId) {
            this.socket.emit('leave', { order_id: this.currentOrderId });
        }
        this.currentOrderId = null;
    }
}

// Chat widget for customer support
class SupportChat {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.init();
    }
    
    init() {
        this.createChatWidget();
        this.setupEventListeners();
    }
    
    createChatWidget() {
        // Create chat widget HTML
        const chatWidget = document.createElement('div');
        chatWidget.id = 'support-chat-widget';
        chatWidget.className = 'support-chat-widget';
        chatWidget.innerHTML = `
            <div class="chat-widget-header" id="chat-widget-toggle">
                <i class="fas fa-comments"></i>
                <span>Chat with us</span>
                <div class="chat-widget-close" style="display: none;">
                    <i class="fas fa-times"></i>
                </div>
            </div>
            <div class="chat-widget-body" id="chat-widget-body" style="display: none;">
                <div class="chat-widget-messages" id="chat-widget-messages">
                    <div class="support-message">
                        <div class="message-content admin">
                            Hello! How can we help you today?
                        </div>
                    </div>
                </div>
                <div class="chat-widget-input">
                    <input type="text" id="support-chat-input" placeholder="Type your message...">
                    <button type="button" id="support-chat-send">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
        `;
        
        // Add styles
        const styles = `
            .support-chat-widget {
                position: fixed;
                bottom: 80px;
                right: 20px;
                width: 300px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
                z-index: 9999;
                font-family: 'Lato', sans-serif;
            }
            
            .chat-widget-header {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 15px;
                border-radius: 10px 10px 0 0;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .chat-widget-header i {
                margin-right: 8px;
            }
            
            .chat-widget-body {
                height: 350px;
                display: flex;
                flex-direction: column;
            }
            
            .chat-widget-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                max-height: 250px;
            }
            
            .support-message {
                margin-bottom: 10px;
            }
            
            .message-content {
                padding: 8px 12px;
                border-radius: 15px;
                max-width: 85%;
                word-wrap: break-word;
            }
            
            .message-content.admin {
                background: #f1f3f4;
                margin-right: auto;
            }
            
            .message-content.user {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                margin-left: auto;
            }
            
            .chat-widget-input {
                display: flex;
                padding: 15px;
                border-top: 1px solid #eee;
                border-radius: 0 0 10px 10px;
            }
            
            .chat-widget-input input {
                flex: 1;
                border: 1px solid #ddd;
                border-radius: 20px;
                padding: 8px 15px;
                margin-right: 10px;
                outline: none;
            }
            
            .chat-widget-input button {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                border: none;
                border-radius: 50%;
                width: 35px;
                height: 35px;
                cursor: pointer;
            }
            
            @media (max-width: 768px) {
                .support-chat-widget {
                    width: calc(100vw - 40px);
                    right: 20px;
                    left: 20px;
                }
            }
        `;
        
        // Add styles to document
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
        
        // Add widget to document
        document.body.appendChild(chatWidget);
    }
    
    setupEventListeners() {
        const toggle = document.getElementById('chat-widget-toggle');
        const body = document.getElementById('chat-widget-body');
        const input = document.getElementById('support-chat-input');
        const sendBtn = document.getElementById('support-chat-send');
        
        toggle.addEventListener('click', () => {
            this.toggleChat();
        });
        
        sendBtn.addEventListener('click', () => {
            this.sendSupportMessage();
        });
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendSupportMessage();
            }
        });
    }
    
    toggleChat() {
        const body = document.getElementById('chat-widget-body');
        const closeIcon = document.querySelector('.chat-widget-close');
        
        this.isOpen = !this.isOpen;
        
        if (this.isOpen) {
            body.style.display = 'flex';
            closeIcon.style.display = 'block';
        } else {
            body.style.display = 'none';
            closeIcon.style.display = 'none';
        }
    }
    
    sendSupportMessage() {
        const input = document.getElementById('support-chat-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Display user message
        this.displaySupportMessage(message, 'user');
        
        // Clear input
        input.value = '';
        
        // Simulate support response (in real app, this would be actual chat system)
        setTimeout(() => {
            this.displaySupportMessage(
                "Thank you for your message! A support representative will be with you shortly. You can also reach us at support@professionalwriters.com or call +91-XXX-XXX-XXXX.",
                'admin'
            );
        }, 1000);
    }
    
    displaySupportMessage(message, type) {
        const messagesContainer = document.getElementById('chat-widget-messages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'support-message';
        messageDiv.innerHTML = `
            <div class="message-content ${type}">
                ${message}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// Initialize chat systems when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize main chat system for logged-in users
    if (document.getElementById('chat-container')) {
        window.chatSystem = new ChatSystem();
    }
    
    // Initialize support chat widget for all users
    window.supportChat = new SupportChat();
});

// Export for global use
window.ChatSystem = ChatSystem;
window.SupportChat = SupportChat;
