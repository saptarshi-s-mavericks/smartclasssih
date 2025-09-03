import React, { useState, useRef, useEffect } from 'react';
import { 
  Modal, 
  Input, 
  Button, 
  Typography, 
  Space, 
  Avatar, 
  Spin,
  message,
  Card
} from 'antd';
import { 
  SendOutlined, 
  RobotOutlined, 
  UserOutlined,
  CloseOutlined
} from '@ant-design/icons';
import { qaService } from '../services/qaService';

const { TextArea } = Input;
const { Text } = Typography;

const SmartQAChat = ({ visible, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize chat session
  useEffect(() => {
    if (visible && !sessionId) {
      initializeChat();
    }
  }, [visible, sessionId]);

  const initializeChat = async () => {
    try {
      const session = await qaService.createChatSession();
      setSessionId(session.session_id);
      
      // Add welcome message
      setMessages([
        {
          id: 1,
          type: 'assistant',
          content: `Hello! I'm your AI assistant for Campus Ecosystem. I can help you with questions about:
          
• Academic schedules and timetables
• Attendance policies and procedures  
• Exam schedules and results
• Department information
• General campus policies
• And much more!

How can I help you today?`,
          timestamp: new Date()
        }
      ]);
    } catch (error) {
      console.error('Failed to initialize chat:', error);
      message.error('Failed to initialize chat session');
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await qaService.sendMessage(sessionId, inputValue.trim());
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.response,
        timestamp: new Date(),
        confidence: response.confidence_score,
        sources: response.knowledge_sources
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      message.error('Failed to get response. Please try again.');
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'I apologize, but I encountered an error while processing your request. Please try again or rephrase your question.',
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatMessage = (content) => {
    // Simple formatting for better readability
    return content.split('\n').map((line, index) => (
      <div key={index} style={{ marginBottom: line.trim() ? '8px' : '4px' }}>
        {line.trim() || <br />}
      </div>
    ));
  };

  const renderMessage = (message) => {
    const isUser = message.type === 'user';
    
    return (
      <div
        key={message.id}
        style={{
          display: 'flex',
          marginBottom: '16px',
          justifyContent: isUser ? 'flex-end' : 'flex-start'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'flex-start', maxWidth: '80%' }}>
          {!isUser && (
            <Avatar 
              icon={<RobotOutlined />} 
              style={{ 
                backgroundColor: '#1890ff', 
                marginRight: '12px',
                marginTop: '4px'
              }} 
            />
          )}
          
          <Card
            size="small"
            style={{
              backgroundColor: isUser ? '#1890ff' : '#f0f2f5',
              color: isUser ? 'white' : 'inherit',
              borderRadius: '12px',
              border: 'none',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
            }}
            bodyStyle={{ padding: '12px 16px' }}
          >
            <div style={{ whiteSpace: 'pre-line' }}>
              {formatMessage(message.content)}
            </div>
            
            {message.confidence && (
              <div style={{ 
                marginTop: '8px', 
                fontSize: '12px', 
                opacity: 0.7,
                color: isUser ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.6)'
              }}>
                Confidence: {Math.round(message.confidence * 100)}%
              </div>
            )}
            
            {message.sources && message.sources.length > 0 && (
              <div style={{ 
                marginTop: '8px', 
                fontSize: '12px', 
                opacity: 0.7,
                color: isUser ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.6)'
              }}>
                Sources: {message.sources.join(', ')}
              </div>
            )}
            
            <div style={{ 
              marginTop: '8px', 
              fontSize: '11px', 
              opacity: 0.6,
              color: isUser ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.5)'
            }}>
              {message.timestamp.toLocaleTimeString()}
            </div>
          </Card>
          
          {isUser && (
            <Avatar 
              icon={<UserOutlined />} 
              style={{ 
                backgroundColor: '#52c41a', 
                marginLeft: '12px',
                marginTop: '4px'
              }} 
            />
          )}
        </div>
      </div>
    );
  };

  return (
    <Modal
      title={
        <Space>
          <RobotOutlined style={{ color: '#1890ff' }} />
          <span>Smart Q&A Assistant</span>
        </Space>
      }
      open={visible}
      onCancel={onClose}
      footer={null}
      width={600}
      style={{ top: 20 }}
      bodyStyle={{ 
        padding: '16px 0',
        height: '70vh',
        display: 'flex',
        flexDirection: 'column'
      }}
    >
      {/* Messages Container */}
      <div style={{ 
        flex: 1, 
        overflowY: 'auto', 
        padding: '0 16px 16px 16px',
        marginBottom: '16px'
      }}>
        {messages.map(renderMessage)}
        
        {loading && (
          <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: '16px' }}>
            <Avatar 
              icon={<RobotOutlined />} 
              style={{ 
                backgroundColor: '#1890ff', 
                marginRight: '12px',
                marginTop: '4px'
              }} 
            />
            <Card
              size="small"
              style={{
                backgroundColor: '#f0f2f5',
                borderRadius: '12px',
                border: 'none'
              }}
              bodyStyle={{ padding: '12px 16px' }}
            >
              <Space>
                <Spin size="small" />
                <Text>Thinking...</Text>
              </Space>
            </Card>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div style={{ padding: '0 16px' }}>
        <div style={{ display: 'flex', gap: '8px' }}>
          <TextArea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything about campus life, academics, or policies..."
            autoSize={{ minRows: 1, maxRows: 4 }}
            disabled={loading}
            style={{ borderRadius: '20px' }}
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || loading}
            style={{ borderRadius: '50%', width: '40px', height: '40px' }}
          />
        </div>
        
        <div style={{ 
          marginTop: '8px', 
          fontSize: '12px', 
          color: '#999',
          textAlign: 'center'
        }}>
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </Modal>
  );
};

export default SmartQAChat;
