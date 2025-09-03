const API_BASE_URL = 'http://localhost:8000/api';

export const qaService = {
  async sendMessage(message) {
    try {
      const response = await fetch(`${API_BASE_URL}/qa/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to send message');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      // For demo purposes, return a mock response
      return {
        response: "I'm the AI assistant for the Campus Ecosystem. I can help you with questions about timetables, attendance, academics, and general campus information. How can I help you today?",
        timestamp: new Date().toISOString()
      };
    }
  },

  async getChatHistory() {
    try {
      const response = await fetch(`${API_BASE_URL}/qa/chat/history/`);
      
      if (!response.ok) {
        throw new Error('Failed to get chat history');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      // Return empty array for demo
      return [];
    }
  },
};
