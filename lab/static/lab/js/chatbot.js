/**
 * VirtualLab Chatbot Widget
 * Clean, simple chatbot for student assistance
 */

class ChatbotWidget {
  constructor() {
    this.isOpen = false;
    this.isLoading = false;
    this.messageHistory = [];
    this.init();
  }

  init() {
    this.createDOM();
    this.attachListeners();
  }

  createDOM() {
    const container = document.createElement('div');
    container.id = 'chatbot-container';
    container.innerHTML = `
      <style>
        ${this.getStyles()}
      </style>
      <div id="chatbot-widget">
        <button id="chatbot-btn" class="chatbot-btn" title="Open chat">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
        
        <div id="chatbot-panel" class="chatbot-panel hidden">
          <div class="chatbot-header">
            <h3>Chat with AI</h3>
            <button id="chatbot-close" class="close-btn">&times;</button>
          </div>
          <div id="chatbot-messages" class="chatbot-messages">
            <div class="message bot-msg">
              <div class="msg-text">Hi! How can I help you today? 👋</div>
            </div>
          </div>
          <form id="chatbot-form" class="chatbot-form">
            <input 
              type="text" 
              id="chatbot-input" 
              placeholder="Ask me anything..."
              autocomplete="off"
            />
            <button type="submit" class="send-btn" title="Send">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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

  getStyles() {
    return `
      #chatbot-widget {
        position: fixed;
        bottom: 24px;
        right: 24px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        z-index: 9999;
      }

      .chatbot-btn {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4f7aff, #7c5cfc);
        border: none;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(79, 122, 255, 0.4);
        transition: all 0.3s;
      }

      .chatbot-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(79, 122, 255, 0.5);
      }

      .chatbot-btn svg {
        width: 24px;
        height: 24px;
      }

      .chatbot-btn.hidden {
        display: none;
      }

      .chatbot-panel {
        position: absolute;
        bottom: 80px;
        right: 0;
        width: 360px;
        height: 500px;
        background: #0f1525;
        border: 1px solid #252d45;
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        opacity: 1;
        transform: scale(1);
        transform-origin: bottom right;
        transition: all 0.3s ease;
      }

      .chatbot-panel.hidden {
        opacity: 0;
        transform: scale(0.8);
        pointer-events: none;
      }

      .chatbot-header {
        padding: 16px;
        border-bottom: 1px solid #252d45;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(79, 122, 255, 0.05);
      }

      .chatbot-header h3 {
        margin: 0;
        font-size: 16px;
        color: #e8ecf4;
      }

      .close-btn {
        background: none;
        border: none;
        color: #9ba3bb;
        font-size: 24px;
        cursor: pointer;
        padding: 0;
        width: 24px;
        height: 24px;
      }

      .close-btn:hover {
        color: #e8ecf4;
      }

      .chatbot-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }

      .chatbot-messages::-webkit-scrollbar {
        width: 4px;
      }

      .chatbot-messages::-webkit-scrollbar-thumb {
        background: #252d45;
        border-radius: 2px;
      }

      .message {
        display: flex;
        animation: fadeIn 0.3s ease;
      }

      .user-msg {
        justify-content: flex-end;
      }

      .bot-msg {
        justify-content: flex-start;
      }

      .msg-text {
        max-width: 80%;
        padding: 10px 14px;
        border-radius: 12px;
        line-height: 1.5;
        font-size: 14px;
        word-wrap: break-word;
        white-space: pre-wrap;
      }

      .user-msg .msg-text {
        background: linear-gradient(135deg, #4f7aff, #7c5cfc);
        color: white;
        border-radius: 12px 4px 12px 12px;
      }

      .bot-msg .msg-text {
        background: #1c2338;
        color: #e8ecf4;
        border: 1px solid #252d45;
        border-radius: 4px 12px 12px 12px;
      }

      .loading {
        display: flex;
        align-items: center;
        gap: 4px;
      }

      .loading-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #4f7aff;
        animation: bounce 1.4s infinite;
      }

      .loading-dot:nth-child(2) {
        animation-delay: 0.2s;
      }

      .loading-dot:nth-child(3) {
        animation-delay: 0.4s;
      }

      @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
      }

      @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }

      .chatbot-form {
        padding: 12px;
        border-top: 1px solid #252d45;
        display: flex;
        gap: 8px;
      }

      #chatbot-input {
        flex: 1;
        background: #141929;
        border: 1px solid #252d45;
        border-radius: 8px;
        padding: 10px 12px;
        color: #e8ecf4;
        font-size: 14px;
        font-family: inherit;
      }

      #chatbot-input:focus {
        outline: none;
        border-color: #4f7aff;
        box-shadow: 0 0 0 2px rgba(79, 122, 255, 0.1);
      }

      #chatbot-input::placeholder {
        color: #636b85;
      }

      .send-btn {
        background: linear-gradient(135deg, #4f7aff, #7c5cfc);
        border: none;
        border-radius: 8px;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: white;
        transition: all 0.2s;
        flex-shrink: 0;
      }

      .send-btn:hover:not(:disabled) {
        transform: scale(1.05);
      }

      .send-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }

      .send-btn svg {
        width: 18px;
        height: 18px;
      }

      @media (max-width: 480px) {
        .chatbot-panel {
          width: calc(100vw - 32px);
          max-width: 360px;
        }
      }
    `;
  }

  attachListeners() {
    const btn = document.getElementById('chatbot-btn');
    const closeBtn = document.getElementById('chatbot-close');
    const form = document.getElementById('chatbot-form');
    
    btn.addEventListener('click', () => this.toggle());
    closeBtn.addEventListener('click', () => this.close());
    form.addEventListener('submit', (e) => this.handleSubmit(e));
  }

  toggle() {
    this.isOpen ? this.close() : this.open();
  }

  open() {
    this.isOpen = true;
    document.getElementById('chatbot-btn').classList.add('hidden');
    document.getElementById('chatbot-panel').classList.remove('hidden');
    document.getElementById('chatbot-input').focus();
  }

  close() {
    this.isOpen = false;
    document.getElementById('chatbot-btn').classList.remove('hidden');
    document.getElementById('chatbot-panel').classList.add('hidden');
  }

  getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  async handleSubmit(e) {
    e.preventDefault();
    
    const input = document.getElementById('chatbot-input');
    const form = document.getElementById('chatbot-form');
    const message = input.value.trim();
    
    if (!message || this.isLoading) return;

    // Disable form
    this.isLoading = true;
    input.disabled = true;
    form.querySelector('.send-btn').disabled = true;

    // Add user message
    this.addMessage(message, 'user');
    input.value = '';

    // Show loading
    const loadingId = this.showLoading();

    try {
      const csrftoken = this.getCookie('csrftoken');
      const headers = {
        'Content-Type': 'application/json',
      };
      
      // Add CSRF token if available
      if (csrftoken) {
        headers['X-CSRFToken'] = csrftoken;
      }

      const response = await fetch('/api/chatbot/', {
        method: 'POST',
        headers: headers,
        credentials: 'same-origin',
        body: JSON.stringify({ message })
      });

      // If the server returned non-JSON (e.g. a login page HTML), avoid parsing as JSON
      const contentType = response.headers.get('content-type') || '';
      if (!contentType.includes('application/json')) {
        // Remove loading indicator
        document.getElementById(loadingId)?.remove();

        // Likely redirected to login page (302 -> HTML response)
        const loginUrl = response.url && response.url.includes('/login') ? response.url : '/login/';
        this.addHtmlMessage(`🔒 You must be logged in to use the chat. <a href="${loginUrl}" target="_blank" rel="noopener">Log in</a>`, 'bot');

        return;
      }

      const data = await response.json();

      // Remove loading indicator
      document.getElementById(loadingId)?.remove();

      if (!response.ok) {
        let errorMsg = data.error || 'Failed to get response';
        if (response.status === 429) {
          errorMsg = `⏳ ${data.error}`;
        }
        this.addMessage(`${errorMsg}`, 'bot');
        return;
      }

      if (data.response) {
        this.addMessage(data.response, 'bot');
      }
    } catch (error) {
      document.getElementById(loadingId)?.remove();
      this.addMessage(`❌ Network error: ${error.message}`, 'bot');
      console.error('Chatbot error:', error);
    } finally {
      this.isLoading = false;
      input.disabled = false;
      form.querySelector('.send-btn').disabled = false;
      input.focus();
      this.scrollToBottom();
    }
  }

  addMessage(text, sender) {
    const container = document.getElementById('chatbot-messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-msg`;

    const textDiv = document.createElement('div');
    textDiv.className = 'msg-text';
    textDiv.textContent = text;

    msgDiv.appendChild(textDiv);
    container.appendChild(msgDiv);
    this.scrollToBottom();
  }

  // Add an HTML message (allows links/buttons inside chat for login)
  addHtmlMessage(html, sender) {
    const container = document.getElementById('chatbot-messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-msg`;

    const textDiv = document.createElement('div');
    textDiv.className = 'msg-text';
    textDiv.innerHTML = html;

    msgDiv.appendChild(textDiv);
    container.appendChild(msgDiv);
    this.scrollToBottom();
  }

  showLoading() {
    const id = `loading-${Date.now()}`;
    const container = document.getElementById('chatbot-messages');
    const msgDiv = document.createElement('div');
    msgDiv.id = id;
    msgDiv.className = 'message bot-msg';

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = '<div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div>';

    msgDiv.appendChild(loadingDiv);
    container.appendChild(msgDiv);
    this.scrollToBottom();
    return id;
  }

  scrollToBottom() {
    const container = document.getElementById('chatbot-messages');
    container.scrollTop = container.scrollHeight;
  }
}

// Initialize when DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new ChatbotWidget());
} else {
  new ChatbotWidget();
}

