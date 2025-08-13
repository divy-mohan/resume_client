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
                bottom: 1%;
                left: 20px;
                width: 280px;
                max-width: calc(100vw - 40px);
                background: white;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.15);
                z-index: 9998;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                border: 1px solid rgba(74, 144, 226, 0.1);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                transform: scale(0.9);
            }
            
            .support-chat-widget:hover {
                box-shadow: 0 12px 40px rgba(0,0,0,0.2);
            }
            
            .chat-widget-header {
                background: linear-gradient(135deg, #4A90E2 0%, #87CEEB 100%);
                color: white;
                padding: 12px 16px;
                border-radius: 12px 12px 0 0;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: space-between;
                transition: all 0.3s ease;
                user-select: none;
                font-size: 0.9rem;
            }
            
            .chat-widget-header:hover {
                background: linear-gradient(135deg, #3A80D2 0%, #77BEDB 100%);
            }
            
            .chat-widget-header i {
                margin-right: 8px;
                font-size: 0.95rem;
            }
            
            .chat-widget-header span {
                font-weight: 600;
                font-size: 1rem;
            }
            
            .chat-widget-close {
                opacity: 0.8;
                transition: opacity 0.3s ease;
            }
            
            .chat-widget-close:hover {
                opacity: 1;
            }
            
            .chat-widget-body {
                height: 400px;
                display: flex;
                flex-direction: column;
                background: #fafbfc;
            }
            
            .chat-widget-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                max-height: 300px;
                background: white;
                scrollbar-width: thin;
                scrollbar-color: #e0e7ff #f8fafc;
            }
            
            .chat-widget-messages::-webkit-scrollbar {
                width: 6px;
            }
            
            .chat-widget-messages::-webkit-scrollbar-track {
                background: #f8fafc;
                border-radius: 3px;
            }
            
            .chat-widget-messages::-webkit-scrollbar-thumb {
                background: #e0e7ff;
                border-radius: 3px;
            }
            
            .chat-widget-messages::-webkit-scrollbar-thumb:hover {
                background: #c7d2fe;
            }
            
            .support-message {
                margin-bottom: 16px;
                animation: fadeInUp 0.3s ease;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .message-content {
                padding: 12px 16px;
                border-radius: 18px;
                max-width: 85%;
                word-wrap: break-word;
                font-size: 0.9rem;
                line-height: 1.4;
                position: relative;
            }
            
            .message-content.admin {
                background: #f1f5f9;
                color: #334155;
                margin-right: auto;
                border-bottom-left-radius: 6px;
            }
            
            .message-content.user {
                background: linear-gradient(135deg, #4A90E2 0%, #87CEEB 100%);
                color: white;
                margin-left: auto;
                border-bottom-right-radius: 6px;
            }
            
            .chat-widget-input {
                display: flex;
                padding: 12px 16px;
                border-top: 1px solid #e2e8f0;
                border-radius: 0 0 12px 12px;
                background: white;
                gap: 8px;
                align-items: center;
            }
            .chat-widget-input input {
                flex: 1;
                border: 1.5px solid #e2e8f0;
                border-radius: 20px;
                padding: 8px 14px;
                outline: none;
                font-size: 0.85rem;
                transition: all 0.3s ease;
                background: #f8fafc;
                height: 32px;
            }   background: #f8fafc;
            }
            
            .chat-widget-input input:focus {
                border-color: #4A90E2;
                background: white;
                box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
            }
            
            .chat-widget-input input::placeholder {
                color: #94a3b8;
            }
            .chat-widget-input button {
                background: linear-gradient(135deg, #4A90E2 0%, #87CEEB 100%);
                color: white;
                border: none;
                border-radius: 50%;
                width: 32px;
                height: 32px;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                font-size: 0.85rem;
            }   flex-shrink: 0;
            }
            
            .chat-widget-input button:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
            }
            
            .chat-widget-input button:active {
                transform: scale(0.95);
            }
            
            .chat-widget-input button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            
            .typing-indicator .typing-dots {
                display: flex;
                gap: 4px;
                align-items: center;
            }
            
            .typing-dots span {
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background: #94a3b8;
                animation: typing 1.4s infinite;
            }
            
            .typing-dots span:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .typing-dots span:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes typing {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.4;
                }
                30% {
                    transform: translateY(-10px);
                    opacity: 1;
                }
            }
            
            .message-time {
                font-size: 0.75rem;
                opacity: 0.7;
                margin-top: 4px;
            }
            
            /* Mobile Responsive */
            @media (max-width: 768px) {
                .support-chat-widget {
                    width: calc(100vw - 20px);
                    left: 10px;
                    bottom: 90px;
                    max-height: calc(100vh - 120px);
                }
                
                .chat-widget-body {
                    height: min(400px, calc(100vh - 200px));
                }
                
                .chat-widget-messages {
                    max-height: calc(100vh - 280px);
                }
            }
            
            @media (max-width: 480px) {
                .support-chat-widget {
                    width: calc(100vw - 16px);
                    left: 8px;
                    bottom: 85px;
                }
                
                .chat-widget-header {
                    padding: 14px 16px;
                }
                
                .chat-widget-input {
                    padding: 12px 16px;
                }
                
                .chat-widget-messages {
                    padding: 16px;
                }
            }
            
            /* High DPI screens */
            @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
                .support-chat-widget {
                    border: 0.5px solid rgba(74, 144, 226, 0.1);
                }
            }
            
            /* Dark mode support */
            @media (prefers-color-scheme: dark) {
                .support-chat-widget {
                    background: #1e293b;
                    border-color: rgba(148, 163, 184, 0.2);
                }
                
                .chat-widget-body {
                    background: #0f172a;
                }
                
                .chat-widget-messages {
                    background: #1e293b;
                }
                
                .message-content.admin {
                    background: #334155;
                    color: #e2e8f0;
                }
                
                .chat-widget-input {
                    background: #1e293b;
                    border-color: rgba(148, 163, 184, 0.2);
                }
                
                .chat-widget-input input {
                    background: #0f172a;
                    border-color: rgba(148, 163, 184, 0.3);
                    color: #e2e8f0;
                }
                
                .chat-widget-input input:focus {
                    background: #1e293b;
                    border-color: #4A90E2;
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
        
        // Toggle chat on click and keyboard events
        toggle.addEventListener('click', () => {
            this.toggleChat();
        });
        
        toggle.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.toggleChat();
            }
        });
        
        // Send message events
        sendBtn.addEventListener('click', () => {
            this.sendSupportMessage();
        });
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendSupportMessage();
            }
        });
        
        // Close chat with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.toggleChat();
            }
        });
        
        // Prevent chat from closing when clicking inside
        body.addEventListener('click', (e) => {
            e.stopPropagation();
        });
        
        // Auto-resize input based on content
        input.addEventListener('input', () => {
            this.adjustInputHeight();
        });
    }
    
    toggleChat() {
        const body = document.getElementById('chat-widget-body');
        const closeIcon = document.querySelector('.chat-widget-close');
        const widget = document.getElementById('support-chat-widget');
        
        this.isOpen = !this.isOpen;
        
        if (this.isOpen) {
            body.style.display = 'flex';
            closeIcon.style.display = 'block';
            widget.style.transform = 'translateY(0)';
            
            // Focus on input after opening
            setTimeout(() => {
                const input = document.getElementById('support-chat-input');
                if (input) input.focus();
            }, 300);
        } else {
            body.style.display = 'none';
            closeIcon.style.display = 'none';
            widget.style.transform = 'translateY(10px)';
        }
    }
    
    sendSupportMessage() {
        const input = document.getElementById('support-chat-input');
        const sendBtn = document.getElementById('support-chat-send');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Disable send button temporarily
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin" aria-hidden="true"></i>';
        
        // Display user message
        this.displaySupportMessage(message, 'user');
        
        // Clear input and reset height
        input.value = '';
        input.style.height = 'auto';
        
        // Simulate typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'support-message typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-content admin">
                <div class="typing-dots">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        
        const messagesContainer = document.getElementById('chat-widget-messages');
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Simulate support response (in real app, this would be actual chat system)
        setTimeout(() => {
            // Remove typing indicator
            messagesContainer.removeChild(typingDiv);
            
            // Add response based on message content
            let response;
            const lowerMessage = message.toLowerCase();
            
            if (lowerMessage.includes('price') || lowerMessage.includes('cost')) {
                response = "Our resume writing packages start from ₹2,999. You can view detailed pricing on our pricing page or I can connect you with our team for a personalized quote.";
            } else if (lowerMessage.includes('time') || lowerMessage.includes('delivery')) {
                response = "We typically deliver resumes within 2-7 working days depending on the package. Rush delivery options are available for urgent requirements.";
            } else if (lowerMessage.includes('sample') || lowerMessage.includes('example')) {
                response = "You can view our sample work on the samples page. Each sample showcases our professional writing style and ATS optimization.";
            } else {
                response = "Thank you for your message! A support representative will be with you shortly. You can also reach us at support@professionalwriters.com or WhatsApp +91-8982737964.";
            }
            
            this.displaySupportMessage(response, 'admin');
            
            // Re-enable send button
            sendBtn.disabled = false;
            sendBtn.innerHTML = '<i class="fas fa-paper-plane" aria-hidden="true"></i>';
            
        }, 1500 + Math.random() * 1000); // Random delay for more natural feel
    }
    
    displaySupportMessage(message, type) {
        const messagesContainer = document.getElementById('chat-widget-messages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'support-message';
        messageDiv.setAttribute('role', 'article');
        
        const timestamp = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        messageDiv.innerHTML = `
            <div class="message-content ${type}" aria-label="${type === 'user' ? 'Your message' : 'Support message'} at ${timestamp}">
                ${this.escapeHtml(message)}
                <div class="message-time" style="font-size: 0.75rem; opacity: 0.7; margin-top: 4px;">${timestamp}</div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Announce new messages to screen readers
        if (type === 'admin') {
            this.announceMessage(message);
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    announceMessage(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'assertive');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.style.position = 'absolute';
        announcement.style.left = '-10000px';
        announcement.textContent = `New message: ${message}`;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }
    
    adjustInputHeight() {
        const input = document.getElementById('support-chat-input');
        if (input) {
            input.style.height = 'auto';
            input.style.height = Math.min(input.scrollHeight, 100) + 'px';
        }
    }
}

// Initialize chat systems when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize main chat system for logged-in users
    if (document.getElementById('chat-container')) {
        window.chatSystem = new ChatSystem();
    }
    
    // Initialize support chat widget for all users with a slight delay
    setTimeout(() => {
        window.supportChat = new SupportChat();
    }, 1000);
    
    // Add smooth scroll behavior for better UX
    document.documentElement.style.scrollBehavior = 'smooth';
});

// Export for global use
window.ChatSystem = ChatSystem;
window.SupportChat = SupportChat;
