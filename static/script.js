const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const fileInput = document.getElementById('file-upload');
const previewContainer = document.getElementById('image-preview-container');
const previewImg = document.getElementById('image-preview');
const removeImgBtn = document.getElementById('remove-image');
const micBtn = document.getElementById('mic-btn');
const exportBtn = document.getElementById('export-btn');

// --- Session Logic ---
let sessionId = localStorage.getItem('medisimplify_session');
if (!sessionId) {
    sessionId = 'sess_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('medisimplify_session', sessionId);
}
// SHOW FULL SESSION ID (No substring)
document.getElementById('session-display').textContent = 'Session: ' + sessionId;

// --- PDF Export Logic ---
exportBtn.addEventListener('click', () => {
    window.location.href = `/download_summary/${sessionId}`;
});

// --- Voice Recognition Logic (Speech-to-Text) ---
let recognition;
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
        micBtn.classList.add('recording');
        userInput.placeholder = "Listening...";
    };

    recognition.onend = () => {
        micBtn.classList.remove('recording');
        userInput.placeholder = "Type or speak...";
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = userInput.value ? userInput.value + " " + transcript : transcript;
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight) + 'px';
    };

    micBtn.addEventListener('click', () => {
        if (micBtn.classList.contains('recording')) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });
} else {
    micBtn.style.display = 'none';
    console.log("Web Speech API not supported in this browser.");
}

// --- Image & Chat Logic ---
fileInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImg.src = e.target.result;
            previewContainer.classList.remove('hidden');
        }
        reader.readAsDataURL(file);
    }
});

removeImgBtn.addEventListener('click', clearImageSelection);

function clearImageSelection() {
    fileInput.value = '';
    previewContainer.classList.add('hidden');
    previewImg.src = '';
}

userInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    if (this.value === '') this.style.height = 'auto';
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

async function sendMessage() {
    const text = userInput.value.trim();
    const file = fileInput.files[0];

    if (!text && !file) return;

    // Add User Message to UI
    const userBubbleContent = document.createElement('div');
    if (file) {
        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        img.onload = () => URL.revokeObjectURL(img.src);
        userBubbleContent.appendChild(img);
    }
    if (text) {
        const p = document.createElement('p');
        p.textContent = text;
        userBubbleContent.appendChild(p);
    }
    addMessageElement(userBubbleContent, 'user');

    userInput.value = '';
    userInput.style.height = 'auto';
    clearImageSelection();

    const loadingId = addLoadingIndicator();

    try {
        const formData = new FormData();
        formData.append('message', text);
        formData.append('session_id', sessionId);
        if (file) formData.append('image', file);

        const response = await fetch('/chat', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        removeLoadingIndicator(loadingId);

        if (data.error) {
            addMessage("Sorry, I'm having trouble connecting. Please try again.", 'bot');
        } else {
            let formattedText = data.response
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\n/g, '<br>');
            addMessage(formattedText, 'bot', true);
        }

    } catch (error) {
        removeLoadingIndicator(loadingId);
        addMessage("Network error. Please check your connection.", 'bot');
    }
}

function addMessage(text, sender, isHTML = false) {
    const div = document.createElement('div');
    if (isHTML) div.innerHTML = text;
    else div.textContent = text;
    addMessageElement(div, sender, isHTML);
}

function addMessageElement(contentNode, sender, isHTML = false) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    if (contentNode instanceof HTMLElement) {
        bubble.appendChild(contentNode);
    } else {
        if (isHTML) bubble.innerHTML = contentNode;
        else bubble.textContent = contentNode;
    }

    div.appendChild(bubble);
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addLoadingIndicator() {
    const id = 'loading-' + Date.now();
    const div = document.createElement('div');
    div.className = 'message bot';
    div.id = id;
    div.innerHTML = `
        <div class="bubble">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
}

function removeLoadingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}