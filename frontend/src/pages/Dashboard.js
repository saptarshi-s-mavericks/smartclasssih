import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Card, Typography, Space, Button, Row, Col, Statistic, Avatar } from 'antd';
import { 
  UserOutlined, 
  BookOutlined, 
  CalendarOutlined, 
  TrophyOutlined,
  TeamOutlined,
  RocketOutlined,
  LogoutOutlined,
  SettingOutlined
} from '@ant-design/icons';
import LoadingSpinner from '../components/common/LoadingSpinner';

const { Title, Paragraph } = Typography;

const Dashboard = () => {
  const { user, logout, isAdmin, isFaculty, isStudent, isParent } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect users to their role-specific portal
    if (user) {
      if (isAdmin()) {
        navigate('/admin');
      } else if (isFaculty()) {
        navigate('/faculty');
      } else if (isStudent()) {
        navigate('/student');
      } else if (isParent()) {
        navigate('/parent');
      }
    }
  }, [user, isAdmin, isFaculty, isStudent, isParent, navigate]);

  if (!user) {
    return <LoadingSpinner />;
  }

  const roleInfo = {
    admin: {
      title: 'Administrator',
      description: 'Full system control and analytics',
      icon: <RocketOutlined style={{ fontSize: '3rem', color: '#1890ff' }} />,
      color: '#1890ff',
      features: [
        'User Management',
        'Timetable Generation',
        'System Analytics',
        'Configuration'
      ]
    },
    faculty: {
      title: 'Faculty',
      description: 'Schedule management and student interaction',
      icon: <UserOutlined style={{ fontSize: '3rem', color: '#52c41a' }} />,
      color: '#52c41a',
      features: [
        'Class Schedule',
        'Attendance Management',
        'Student Performance',
        'Assignments'
      ]
    },
    student: {
      title: 'Student',
      description: 'Personal academic dashboard',
      icon: <BookOutlined style={{ fontSize: '3rem', color: '#722ed1' }} />,
      color: '#722ed1',
      features: [
        'My Timetable',
        'Attendance Tracking',
        'Performance Metrics',
        'Assignments'
      ]
    },
    parent: {
      title: 'Parent',
      description: 'Child progress monitoring',
      icon: <TeamOutlined style={{ fontSize: '3rem', color: '#fa8c16' }} />,
      color: '#fa8c16',
      features: [
        'Child Progress',
        'Attendance Reports',
        'Performance Tracking',
        'Communication'
      ]
    }
  };

  const currentRole = roleInfo[user.role];

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const handleProfile = () => {
    // Navigate to profile settings
    navigate(`/${user.role}/profile`);
  };

  return (
    <div style={{ 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header */}
        <Card 
          style={{ 
            marginBottom: '24px',
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            border: 'none',
            borderRadius: '16px'
          }}
        >
          <Row justify="space-between" align="middle">
            <Col>
              <Space>
                {currentRole.icon}
                <div>
                  <Title level={2} style={{ margin: 0, color: currentRole.color }}>
                    Welcome, {user.first_name}!
                  </Title>
                  <Paragraph style={{ margin: 0, color: '#666' }}>
                    {currentRole.description}
                  </Paragraph>
                </div>
              </Space>
            </Col>
            <Col>
              <Space>
                <Button 
                  icon={<SettingOutlined />}
                  onClick={handleProfile}
                >
                  Profile
                </Button>
                <Button 
                  icon={<LogoutOutlined />}
                  onClick={handleLogout}
                  danger
                >
                  Logout
                </Button>
              </Space>
            </Col>
          </Row>
        </Card>

        {/* Role Information */}
        <Row gutter={[24, 24]}>
          <Col xs={24} lg={16}>
            <Card 
              style={{ 
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(10px)',
                border: 'none',
                borderRadius: '16px',
                height: '100%'
              }}
            >
              <Title level={3} style={{ color: currentRole.color, marginBottom: '24px' }}>
                {currentRole.title} Portal Features
              </Title>
              
              <Row gutter={[16, 16]}>
                {currentRole.features.map((feature, index) => (
                  <Col xs={24} sm={12} key={index}>
                    <Card 
                      size="small" 
                      style={{ 
                        border: `2px solid ${currentRole.color}20`,
                        borderRadius: '12px'
                      }}
                    >
                      <div style={{ textAlign: 'center' }}>
                        <div style={{ 
                          width: '40px', 
                          height: '40px', 
                          borderRadius: '50%',
                          backgroundColor: `${currentRole.color}20`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          margin: '0 auto 12px auto'
                        }}>
                          {index === 0 && <CalendarOutlined style={{ color: currentRole.color }} />}
                          {index === 1 && <TrophyOutlined style={{ color: currentRole.color }} />}
                          {index === 2 && <BookOutlined style={{ color: currentRole.color }} />}
                          {index === 3 && <TeamOutlined style={{ color: currentRole.color }} />}
                        </div>
                        <Paragraph style={{ margin: 0, fontWeight: 500 }}>
                          {feature}
                        </Paragraph>
                      </div>
                    </Card>
                  </Col>
                ))}
              </Row>

              <div style={{ marginTop: '32px', textAlign: 'center' }}>
                <Button 
                  type="primary" 
                  size="large"
                  style={{ 
                    backgroundColor: currentRole.color,
                    borderColor: currentRole.color,
                    borderRadius: '8px',
                    height: '48px',
                    padding: '0 32px'
                  }}
                  onClick={() => navigate(`/${user.role}`)}
                >
                  Access {currentRole.title} Portal
                </Button>
              </div>
            </Card>
          </Col>

          <Col xs={24} lg={8}>
            <Card 
              style={{ 
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(10px)',
                border: 'none',
                borderRadius: '16px',
                height: '100%'
              }}
            >
              <Title level={4} style={{ marginBottom: '24px' }}>
                Quick Stats
              </Title>
              
              <Space direction="vertical" style={{ width: '100%' }} size="large">
                <Statistic
                  title="Role"
                  value={currentRole.title}
                  valueStyle={{ color: currentRole.color }}
                />
                
                <Statistic
                  title="Member Since"
                  value={new Date(user.date_joined).toLocaleDateString()}
                />
                
                <Statistic
                  title="Status"
                  value="Active"
                  valueStyle={{ color: '#52c41a' }}
                />
              </Space>

              <div style={{ marginTop: '32px' }}>
                <Title level={5}>Quick Actions</Title>
                <Space direction="vertical" style={{ width: '100%' }} size="small">
                  <Button 
                    block 
                    onClick={() => navigate(`/${user.role}/schedule`)}
                  >
                    View Schedule
                  </Button>
                  <Button 
                    block 
                    onClick={() => navigate(`/${user.role}/attendance`)}
                  >
                    Attendance
                  </Button>
                  <Button 
                    block 
                    onClick={() => navigate(`/${user.role}/performance`)}
                  >
                    Performance
                  </Button>
                </Space>
              </div>
            </Card>
          </Col>
        </Row>

        {/* System Information */}
        <Card 
          style={{ 
            marginTop: '24px',
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            border: 'none',
            borderRadius: '16px'
          }}
        >
          <Title level={4} style={{ marginBottom: '24px' }}>
            Campus Ecosystem System
          </Title>
          
          <Row gutter={[24, 16]}>
            <Col xs={24} sm={8}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ 
                  width: '60px', 
                  height: '60px', 
                  borderRadius: '50%',
                  backgroundColor: '#1890ff20',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 16px auto'
                }}>
                  <RocketOutlined style={{ fontSize: '2rem', color: '#1890ff' }} />
                </div>
                <Title level={5}>Intelligent Scheduling</Title>
                <Paragraph style={{ color: '#666' }}>
                  Advanced constraint satisfaction & optimization
                </Paragraph>
              </div>
            </Col>
            
            <Col xs={24} sm={8}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ 
                  width: '60px', 
                  height: '60px', 
                  borderRadius: '50%',
                  backgroundColor: '#52c41a20',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 16px auto'
                }}>
                  <TeamOutlined style={{ fontSize: '2rem', color: '#52c41a' }} />
                </div>
                <Title level={5}>Role-Based Access</Title>
                <Paragraph style={{ color: '#666' }}>
                  Tailored portals for each user type
                </Paragraph>
              </div>
            </Col>
            
            <Col xs={24} sm={8}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ 
                  width: '60px', 
                  height: '60px', 
                  borderRadius: '50%',
                  backgroundColor: '#722ed120',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 16px auto'
                }}>
                  <TrophyOutlined style={{ fontSize: '2rem', color: '#722ed1' }} />
                </div>
                <Title level={5}>AI-Powered Support</Title>
                <Paragraph style={{ color: '#666' }}>
                  Smart Q&A with Google Gemini
                </Paragraph>
              </div>
            </Col>
          </Row>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
