import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { sendMessage } from '../services/api';
import './ChatInterface.css';

const ChatInterface = () => {

    // =====================================================
    // STATE
    // =====================================================
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState(null);
    const [isLocked, setIsLocked] = useState(false);

    const messagesEndRef = useRef(null);

    // =====================================================
    // LOAD SESSION + HISTORY
    // =====================================================
    useEffect(() => {
        const storedSession = localStorage.getItem('chat_session_id');
        const storedMessages = localStorage.getItem('chat_messages');

        if (storedSession) setSessionId(storedSession);
        if (storedMessages) setMessages(JSON.parse(storedMessages));
    }, []);

    // save messages automatically
    useEffect(() => {
        localStorage.setItem('chat_messages', JSON.stringify(messages));
    }, [messages]);

    // =====================================================
    // AUTO SCROLL
    // =====================================================
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // =====================================================
    // RESET SESSION
    // =====================================================
    const handleEndSession = () => {
        localStorage.removeItem('chat_session_id');
        localStorage.removeItem('chat_messages');

        setSessionId(null);
        setMessages([]);
        setIsLocked(false);
    };

    // =====================================================
    // SEND MESSAGE
    // =====================================================
    const handleSend = async (e) => {
        e.preventDefault();

        if (!input.trim() || isLoading || isLocked) return;

        const userMsg = { role: 'user', content: input };

        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            const data = await sendMessage(userMsg.content, sessionId);

            // update session id
            if (data.session_id && data.session_id !== sessionId) {
                setSessionId(data.session_id);
                localStorage.setItem('chat_session_id', data.session_id);
            }

            // emergency lock detection
            if (data.response.includes("EMERGENCY ALERT")) {
                setIsLocked(true);
            }

            const botMsg = {
                role: 'bot',
                content: data.response
            };

            setMessages(prev => [...prev, botMsg]);

        } catch (error) {
            const errorMsg = {
                role: 'system',
                content:
                    "⚠️ Error: Could not connect to the healthcare assistant. Please try again."
            };

            setMessages(prev => [...prev, errorMsg]);

        } finally {
            setIsLoading(false);
        }
    };

    // =====================================================
    // UI
    // =====================================================
    return (
        <div className="chat-container">

            {/* HEADER */}
            <header className="chat-header">
                <div className="header-row">
                    <div>
                        <h1>HealthGuide AI</h1>
                        <p>Symptom Assessment Assistant</p>
                    </div>

                    {/* ALWAYS VISIBLE RESET BUTTON */}
                    <button
                        className="end-session-btn"
                        onClick={handleEndSession}
                        disabled={!messages.length}
                    >
                        Reset Chat
                    </button>
                </div>
            </header>

            {/* MESSAGE AREA */}
            <div className="messages-area">

                {messages.length === 0 && (
                    <div className="welcome-message">
                        <h2>Hello! 👋</h2>
                        <p>
                            I can help assess your symptoms and provide
                            preliminary guidance.
                        </p>
                        <p>
                            What specific symptoms are you experiencing today?
                        </p>
                        <small>
                            Remember: I cannot provide a medical diagnosis.
                        </small>
                    </div>
                )}

                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`message-bubble ${msg.role}`}
                    >
                        <div className="message-content">
                            {msg.role === 'bot' ? (
                                <ReactMarkdown>
                                    {msg.content}
                                </ReactMarkdown>
                            ) : (
                                <p>{msg.content}</p>
                            )}
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="message-bubble bot loading">
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* INPUT AREA */}
            <form className="input-area" onSubmit={handleSend}>

                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder={
                        isLocked
                            ? "Session paused due to emergency..."
                            : "Describe your symptoms..."
                    }
                    disabled={isLoading || isLocked}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSend(e);
                        }
                    }}
                />

                <button
                    type="submit"
                    disabled={isLoading || !input.trim() || isLocked}
                >
                    ➤
                </button>
            </form>

            {/* DISCLAIMER */}
            <footer className="disclaimer-footer">
                <p>
                    ⚠️ <strong>Disclaimer:</strong> Not a doctor.
                    Educational guidance only.
                    In emergencies, call your local emergency number.
                </p>
            </footer>

        </div>
    );
};

export default ChatInterface;