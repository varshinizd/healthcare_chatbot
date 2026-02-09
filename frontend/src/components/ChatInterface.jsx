import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { sendMessage } from '../services/api';
import './ChatInterface.css'; // We'll create this or use styled components? Let's use CSS modules or just a CSS file for simplicity alongside.

const ChatInterface = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Load session ID from local storage or generate/wait for backend
        const storedSession = localStorage.getItem('chat_session_id');
        if (storedSession) {
            setSessionId(storedSession);
        }
    }, []);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            const data = await sendMessage(userMsg.content, sessionId);

            // Update session ID if new
            if (data.session_id && data.session_id !== sessionId) {
                setSessionId(data.session_id);
                localStorage.setItem('chat_session_id', data.session_id);
            }

            const botMsg = { role: 'bot', content: data.response };
            setMessages(prev => [...prev, botMsg]);
        } catch (error) {
            const errorMsg = { role: 'system', content: "⚠️ Error: Could not connect to the healthcare assistant. Please try again." };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <header className="chat-header">
                <h1>HealthGuide AI</h1>
                <p>Symptom Assessment Assistant</p>
            </header>

            <div className="messages-area">
                {messages.length === 0 && (
                    <div className="welcome-message">
                        <h2>Hello! 👋</h2>
                        <p>I can help assess your symptoms and provide preliminary guidance.</p>
                        <p>What specific symptoms are you experiencing today?</p>
                        <small>Remember: I cannot provide a medical diagnosis.</small>
                    </div>
                )}

                {messages.map((msg, index) => (
                    <div key={index} className={`message-bubble ${msg.role}`}>
                        <div className="message-content">
                            {msg.role === 'bot' ? (
                                <ReactMarkdown>{msg.content}</ReactMarkdown>
                            ) : (
                                <p>{msg.content}</p>
                            )}
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="message-bubble bot loading">
                        <div className="typing-indicator">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form className="input-area" onSubmit={handleSend}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Describe your symptoms..."
                    disabled={isLoading}
                />
                <button type="submit" disabled={isLoading || !input.trim()}>
                    ➤
                </button>
            </form>

            <footer className="disclaimer-footer">
                <p>⚠️ <strong>Disclaimer:</strong> Not a doctor. For educational purposes only. In emergencies, call your local emergency number.</p>
            </footer>
        </div>
    );
};

export default ChatInterface;
