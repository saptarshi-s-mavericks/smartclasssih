import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Button, 
  Card, 
  Row, 
  Col, 
  Typography, 
  Space, 
  Divider,
  Statistic,
  Avatar,
  List,
  Tag,
  Carousel
} from 'antd';
import { 
  UserOutlined, 
  BookOutlined, 
  CalendarOutlined, 
  TrophyOutlined,
  RobotOutlined,
  TeamOutlined,
  SafetyOutlined,
  RocketOutlined
} from '@ant-design/icons';
import SmartQAChat from '../components/SmartQAChat';

const { Title, Paragraph, Text } = Typography;

const LandingPage = () => {
  const navigate = useNavigate();
  const [showChat, setShowChat] = useState(false);

  const features = [
    {
      icon: <BookOutlined style={{ fontSize: '2rem', color: '#1890ff' }} />,
      title: 'Intelligent Scheduling',
      description: 'Advanced constraint satisfaction & optimization for perfect timetables'
    },
    {
      icon: <UserOutlined style={{ fontSize: '2rem', color: '#52c41a' }} />,
      title: 'Role-Based Portals',
      description: 'Tailored dashboards for Admin, Faculty, Students, and Parents'
    },
    {
      icon: <RobotOutlined style={{ fontSize: '2rem', color: '#722ed1' }} />,
      title: 'AI-Powered Support',
      description: '24/7 Smart Q&A Desk with Google Gemini integration'
    },
    {
      icon: <CalendarOutlined style={{ fontSize: '2rem', color: '#fa8c16' }} />,
      title: 'Attendance Management',
      description: 'Real-time tracking with analytics and alerts'
    },
    {
      icon: <TrophyOutlined style={{ fontSize: '2rem', color: '#eb2f96' }} />,
      title: 'Performance Monitoring',
      description: 'Comprehensive academic progress tracking'
    },
    {
      icon: <TeamOutlined style={{ fontSize: '2rem', color: '#13c2c2' }} />,
      title: 'Parental Engagement',
      description: 'Real-time access to child\'s academic progress'
    }
  ];

  const stats = [
    { title: 'Departments', value: 8, suffix: '+' },
    { title: 'Faculty Members', value: 150, suffix: '+' },
    { title: 'Students', value: 2000, suffix: '+' },
    { title: 'Subjects', value: 200, suffix: '+' }
  ];

  const testimonials = [
    {
      name: 'Dr. Sarah Johnson',
      role: 'Dean of Engineering',
      content: 'The intelligent scheduling system has revolutionized how we manage our academic calendar. It\'s like having an expert scheduler working 24/7.',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah'
    },
    {
      name: 'Prof. Michael Chen',
      role: 'Computer Science Faculty',
      content: 'The attendance tracking and performance analytics help me identify at-risk students early and provide timely support.',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Michael'
    },
    {
      name: 'Emily Rodriguez',
      role: 'Student',
      content: 'Having all my academic information in one place makes it so much easier to track my progress and stay organized.',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Emily'
    }
  ];

  const handleLogin = (role) => {
    navigate('/login', { state: { role } });
  };

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section" style={{ 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        padding: '80px 0',
        textAlign: 'center'
      }}>
        <div className="container">
          <Title level={1} style={{ color: 'white', marginBottom: 24 }}>
            Campus Ecosystem
          </Title>
          <Title level={3} style={{ color: 'white', fontWeight: 300, marginBottom: 32 }}>
            The Future of Academic Management
          </Title>
          <Paragraph style={{ fontSize: '18px', marginBottom: 40, color: 'rgba(255,255,255,0.9)' }}>
            A comprehensive digital platform that transforms campus management through intelligent scheduling, 
            role-based portals, and AI-powered support systems.
          </Paragraph>
          <Space size="large">
            <Button 
              type="primary" 
              size="large" 
              icon={<RocketOutlined />}
              onClick={() => handleLogin('admin')}
            >
              Admin Portal
            </Button>
            <Button 
              size="large" 
              icon={<UserOutlined />}
              onClick={() => handleLogin('faculty')}
            >
              Faculty Portal
            </Button>
            <Button 
              size="large" 
              icon={<BookOutlined />}
              onClick={() => handleLogin('student')}
            >
              Student Portal
            </Button>
            <Button 
              size="large" 
              icon={<TeamOutlined />}
              onClick={() => handleLogin('parent')}
            >
              Parent Portal
            </Button>
          </Space>
        </div>
      </section>

      {/* Features Section */}
      <section style={{ padding: '80px 0', backgroundColor: '#f8f9fa' }}>
        <div className="container">
          <Title level={2} style={{ textAlign: 'center', marginBottom: 60 }}>
            Why Choose Campus Ecosystem?
          </Title>
          <Row gutter={[32, 32]}>
            {features.map((feature, index) => (
              <Col xs={24} sm={12} lg={8} key={index}>
                <Card 
                  hoverable 
                  style={{ height: '100%', textAlign: 'center' }}
                  bodyStyle={{ padding: '32px 24px' }}
                >
                  <div style={{ marginBottom: 24 }}>
                    {feature.icon}
                  </div>
                  <Title level={4} style={{ marginBottom: 16 }}>
                    {feature.title}
                  </Title>
                  <Paragraph style={{ color: '#666', margin: 0 }}>
                    {feature.description}
                  </Paragraph>
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      </section>

      {/* Stats Section */}
      <section style={{ padding: '60px 0', backgroundColor: 'white' }}>
        <div className="container">
          <Row gutter={[32, 32]} justify="center">
            {stats.map((stat, index) => (
              <Col key={index}>
                <Statistic
                  title={stat.title}
                  value={stat.value}
                  suffix={stat.suffix}
                  valueStyle={{ color: '#1890ff', fontSize: '2.5rem' }}
                />
              </Col>
            ))}
          </Row>
        </div>
      </section>

      {/* Testimonials Section */}
      <section style={{ padding: '80px 0', backgroundColor: '#f8f9fa' }}>
        <div className="container">
          <Title level={2} style={{ textAlign: 'center', marginBottom: 60 }}>
            What Our Users Say
          </Title>
          <Row gutter={[32, 32]}>
            {testimonials.map((testimonial, index) => (
              <Col xs={24} md={8} key={index}>
                <Card style={{ height: '100%' }}>
                  <div style={{ textAlign: 'center', marginBottom: 24 }}>
                    <Avatar 
                      size={64} 
                      src={testimonial.avatar}
                      style={{ marginBottom: 16 }}
                    />
                    <Title level={4} style={{ margin: 0 }}>
                      {testimonial.name}
                    </Title>
                    <Tag color="blue">{testimonial.role}</Tag>
                  </div>
                  <Paragraph style={{ fontStyle: 'italic', textAlign: 'center' }}>
                    "{testimonial.content}"
                  </Paragraph>
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      </section>

      {/* Smart Q&A Section */}
      <section style={{ padding: '80px 0', backgroundColor: 'white' }}>
        <div className="container">
          <Row gutter={[48, 32]} align="middle">
            <Col xs={24} lg={12}>
              <Title level={2}>
                AI-Powered Support System
              </Title>
              <Paragraph style={{ fontSize: '16px', color: '#666', marginBottom: 24 }}>
                Get instant answers to your questions with our Smart Q&A Desk. 
                Powered by Google Gemini, it provides accurate information about academic policies, 
                schedules, and procedures 24/7.
              </Paragraph>
              <Button 
                type="primary" 
                size="large" 
                icon={<RobotOutlined />}
                onClick={() => setShowChat(true)}
              >
                Try Smart Q&A
              </Button>
            </Col>
            <Col xs={24} lg={12}>
              <div style={{ 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                borderRadius: '16px',
                padding: '40px',
                color: 'white',
                textAlign: 'center'
              }}>
                <RobotOutlined style={{ fontSize: '4rem', marginBottom: '24px' }} />
                <Title level={3} style={{ color: 'white', marginBottom: 16 }}>
                  Smart Q&A Desk
                </Title>
                <Paragraph style={{ color: 'rgba(255,255,255,0.9)', margin: 0 }}>
                  Ask me anything about academics, schedules, policies, or procedures!
                </Paragraph>
              </div>
            </Col>
          </Row>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ 
        backgroundColor: '#001529', 
        color: 'white', 
        padding: '40px 0',
        textAlign: 'center'
      }}>
        <div className="container">
          <Title level={4} style={{ color: 'white', marginBottom: 16 }}>
            Campus Ecosystem
          </Title>
          <Paragraph style={{ color: 'rgba(255,255,255,0.7)', marginBottom: 24 }}>
            Transforming academic management through intelligent technology
          </Paragraph>
          <Space size="large">
            <Button type="link" style={{ color: 'rgba(255,255,255,0.7)' }}>
              Privacy Policy
            </Button>
            <Button type="link" style={{ color: 'rgba(255,255,255,0.7)' }}>
              Terms of Service
            </Button>
            <Button type="link" style={{ color: 'rgba(255,255,255,0.7)' }}>
              Contact Support
            </Button>
          </Space>
        </div>
      </footer>

      {/* Smart Q&A Chat Modal */}
      {showChat && (
        <SmartQAChat 
          visible={showChat}
          onClose={() => setShowChat(false)}
        />
      )}
    </div>
  );
};

export default LandingPage;
