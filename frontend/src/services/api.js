import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const sendMessage = async (message, sessionId) => {
    try {
        const response = await api.post('/chat', {
            message,
            session_id: sessionId
        });
        return response.data;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};
