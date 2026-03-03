/**
 * VirtualLab Chatbot Widget
 * A floating chatbot widget for student assistance
 */

class ChatbotWidget {
  constructor() {
    this.isOpen = false;
    this.messages = [];
    this.isLoading = false;
    this.init();
  }

  init() {
    this.createWidget();
    this.attachEventListeners();
  }

  createWidget() {
    // Create container
    const container = document.createElement('div');
    container.id = 'chatbot-widget';
    container.className = 'chatbot-widget';
    container.innerHTML = `
      <div class="chatbot-button" id="chatbot-toggle" title="Open Chatbot">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </div>
      
      <div class="chatbot-window" id="chatbot-window">
        <div class="chatbot-header">
          <div class="chatbot-title">Chat with VirtualLab</div>
          <button id="chatbot-close" class="chatbot-close" title="Close chatbot">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="chatbot-messages" id="chatbot-messages">
          <div class="message bot-message">
            <div class="message-content">
              👋 Hi! I'm your AI Assistant. How can I help you today?
            </div>
          </div>
        </div>
        
        <div class="chatbot-input-area">
          <form id="chatbot-form" class="chatbot-form">
            <input 
              type="text" 
              id="chatbot-input" 
              class="chatbot-input" 
              placeholder="Ask me anything..."
              autocomplete="off"
            >
            <button type="submit" class="chatbot-send" id="chatbot-send" title="Send message">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </form>
        </div>
      </div>
    `;
    
    document.body.appendChild(container);
  }

  attachEventListeners() {
    const toggleBtn = document.getElementById('chatbot-toggle');
    const closeBtn = document.getElementById('chatbot-close');
    const form = document.getElementById('chatbot-form');
    const input = document.getElementById('chatbot-input');

    toggleBtn.addEventListener('click', () => this.toggle());
    closeBtn.addEventListener('click', () => this.close());
    form.addEventListener('submit', (e) => this.handleSubmit(e));
  }

  toggle() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  }

  open() {
    const widget = document.getElementById('chatbot-widget');
    const window = document.getElementById('chatbot-window');
    this.isOpen = true;
    
    widget.classList.add('open');
    window.classList.add('show');
    
    // Focus on input
    setTimeout(() => {
      document.getElementById('chatbot-input').focus();
    }, 200);
  }

  close() {
    const widget = document.getElementById('chatbot-widget');
    const window = document.getElementById('chatbot-window');
    this.isOpen = false;
    
    widget.classList.remove('open');
    window.classList.remove('show');
  }

  async handleSubmit(e) {
    e.preventDefault();
    
    const input = document.getElementById('chatbot-input');
    const sendBtn = document.getElementById('chatbot-send');
    const message = input.value.trim();
    
    if (!message) return;
    if (this.isLoading) return;

    // Add user message and clear field
    this.addMessage(message, 'user');
    input.value = '';

    // show loading placeholder and disable input/buttons
    this.showLoading();
    input.disabled = true;
    sendBtn.disabled = true;

    this.isLoading = true;
    
    try {
      // Get CSRF token
      const csrfToken = this.getCookie('csrftoken');
      
      const response = await fetch('/api/chatbot/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to get response');
      }

      const data = await response.json();
      this.hideLoading();
      this.addMessage(data.response, 'bot');
    } catch (error) {
      console.error('Chatbot error:', error);
      this.hideLoading();
      this.addMessage(
        '❌ Sorry, I encountered an error. Please try again later.',
        'bot'
      );
    } finally {
      this.isLoading = false;
      input.disabled = false;
      sendBtn.disabled = false;
      input.focus();
    }
  }

  addMessage(text, sender) {
    const messagesContainer = document.getElementById('chatbot-messages');
    
    const messageEl = document.createElement('div');
    messageEl.className = `message ${sender}-message`;
    
    const contentEl = document.createElement('div');
    contentEl.className = 'message-content';
    
    // Parse text as markdown-like content for better formatting
    contentEl.innerHTML = this.formatMessage(text);
    
    messageEl.appendChild(contentEl);
    messagesContainer.appendChild(messageEl);
    
    // Always scroll new message into view
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  showLoading() {
    const messagesContainer = document.getElementById('chatbot-messages');
    // create placeholder message
    const loadingEl = document.createElement('div');
    loadingEl.className = 'message bot-message loading';

    const contentEl = document.createElement('div');
    contentEl.className = 'message-content';
    contentEl.innerHTML = '<div class="loading-spinner"></div>';

    loadingEl.appendChild(contentEl);
    messagesContainer.appendChild(loadingEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    this.loadingEl = loadingEl;
  }

  hideLoading() {
    if (this.loadingEl) {
      this.loadingEl.remove();
      this.loadingEl = null;
    }
  }

  formatMessage(text) {
    // Simple formatting for better readability
    // Bold text: **text** -> <strong>text</strong>
    // Italic text: *text* -> <em>text</em>
    // Line breaks
    
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>')
      .replace(/\n\n/g, '<br><br>');
  }

  getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
}

// Initialize chatbot when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new ChatbotWidget();
  });
} else {
  new ChatbotWidget();
}
