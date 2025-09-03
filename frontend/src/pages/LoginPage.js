import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  Form, 
  Input, 
  Button, 
  Card, 
  Typography, 
  Space, 
  Tabs, 
  message,
  Divider,
  Row,
  Col
} from 'antd';
import { 
  UserOutlined, 
  LockOutlined, 
  MailOutlined,
  BookOutlined,
  TeamOutlined,
  RocketOutlined,
  UserSwitchOutlined
} from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';

const { Title, Paragraph, Text } = Typography;
const { TabPane } = Tabs;

const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, register } = useAuth();
  const [activeTab, setActiveTab] = useState('login');
  const [loading, setLoading] = useState(false);
  const [loginForm] = Form.useForm();
  const [registerForm] = Form.useForm();

  // Get role from navigation state
  const selectedRole = location.state?.role || 'student';

  useEffect(() => {
    // Set default role in register form
    if (selectedRole) {
      registerForm.setFieldsValue({ role: selectedRole });
    }
  }, [selectedRole, registerForm]);

  const handleLogin = async (values) => {
    setLoading(true);
    try {
      const result = await login(values);
      if (result.success) {
        navigate('/dashboard');
      }
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (values) => {
    setLoading(true);
    try {
      const result = await register(values);
      if (result.success) {
        setActiveTab('login');
        loginForm.setFieldsValue({ email: values.email });
        message.success('Registration successful! Please log in.');
      }
    } catch (error) {
      console.error('Registration error:', error);
    } finally {
      setLoading(false);
    }
  };

  const roleInfo = {
    admin: {
      title: 'Administrator',
      description: 'Full system control and analytics',
      icon: <RocketOutlined style={{ fontSize: '2rem', color: '#1890ff' }} />,
      color: '#1890ff'
    },
    faculty: {
      title: 'Faculty',
      description: 'Schedule management and student interaction',
      icon: <UserOutlined style={{ fontSize: '2rem', color: '#52c41a' }} />,
      color: '#52c41a'
    },
    student: {
      title: 'Student',
      description: 'Personal academic dashboard',
      icon: <BookOutlined style={{ fontSize: '2rem', color: '#722ed1' }} />,
      color: '#722ed1'
    },
    parent: {
      title: 'Parent',
      description: 'Child progress monitoring',
      icon: <TeamOutlined style={{ fontSize: '2rem', color: '#fa8c16' }} />,
      color: '#fa8c16'
    }
  };

  const currentRole = roleInfo[selectedRole];

  return (
    <div style={{ 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <Row justify="center" style={{ width: '100%', maxWidth: '1000px' }}>
        <Col xs={24} lg={12}>
          {/* Role Information Card */}
          <Card 
            style={{ 
              height: '100%',
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(10px)',
              border: 'none',
              borderRadius: '16px',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
            }}
            bodyStyle={{ padding: '40px' }}
          >
            <div style={{ textAlign: 'center', marginBottom: '32px' }}>
              {currentRole.icon}
              <Title level={2} style={{ marginTop: '16px', color: currentRole.color }}>
                {currentRole.title} Portal
              </Title>
              <Paragraph style={{ fontSize: '16px', color: '#666' }}>
                {currentRole.description}
              </Paragraph>
            </div>

            <div style={{ marginBottom: '32px' }}>
              <Title level={4}>Welcome to Campus Ecosystem</Title>
              <Paragraph style={{ color: '#666' }}>
                Experience the future of academic management with our intelligent scheduling system, 
                real-time analytics, and AI-powered support.
              </Paragraph>
            </div>

            <div style={{ 
              background: '#f8f9fa', 
              padding: '20px', 
              borderRadius: '12px',
              border: `2px solid ${currentRole.color}20`
            }}>
              <Title level={5} style={{ color: currentRole.color, marginBottom: '16px' }}>
                Key Features for {currentRole.title}s
              </Title>
              <ul style={{ paddingLeft: '20px', margin: 0 }}>
                {currentRole.title === 'Administrator' && (
                  <>
                    <li>Full system control and user management</li>
                    <li>Advanced analytics and reporting</li>
                    <li>Timetable generation and approval</li>
                    <li>System configuration and monitoring</li>
                  </>
                )}
                {currentRole.title === 'Faculty' && (
                  <>
                    <li>Personalized class schedules</li>
                    <li>Attendance tracking and management</li>
                    <li>Student performance monitoring</li>
                    <li>Assignment and exam management</li>
                  </>
                )}
                {currentRole.title === 'Student' && (
                  <>
                    <li>Personal academic dashboard</li>
                    <li>Class schedules and attendance</li>
                    <li>Performance tracking and goals</li>
                    <li>Assignment submissions</li>
                  </>
                )}
                {currentRole.title === 'Parent' && (
                  <>
                    <li>Real-time child progress monitoring</li>
                    <li>Attendance and performance tracking</li>
                    <li>Communication with faculty</li>
                    <li>Academic calendar access</li>
                  </>
                )}
              </ul>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          {/* Authentication Card */}
          <Card 
            style={{ 
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(10px)',
              border: 'none',
              borderRadius: '16px',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
              marginTop: { xs: '20px', lg: '0' }
            }}
            bodyStyle={{ padding: '40px' }}
          >
            <div style={{ textAlign: 'center', marginBottom: '32px' }}>
              <Title level={2} style={{ color: currentRole.color }}>
                {activeTab === 'login' ? 'Sign In' : 'Create Account'}
              </Title>
              <Paragraph style={{ color: '#666' }}>
                {activeTab === 'login' 
                  ? `Access your ${currentRole.title.toLowerCase()} portal` 
                  : `Join Campus Ecosystem as a ${currentRole.title.toLowerCase()}`
                }
              </Paragraph>
            </div>

            <Tabs 
              activeKey={activeTab} 
              onChange={setActiveTab}
              centered
              style={{ marginBottom: '24px' }}
            >
              <TabPane 
                tab={
                  <span>
                    <UserSwitchOutlined />
                    Sign In
                  </span>
                } 
                key="login"
              >
                <Form
                  form={loginForm}
                  onFinish={handleLogin}
                  layout="vertical"
                  size="large"
                >
                  <Form.Item
                    name="email"
                    label="Email"
                    rules={[
                      { required: true, message: 'Please enter your email!' },
                      { type: 'email', message: 'Please enter a valid email!' }
                    ]}
                  >
                    <Input 
                      prefix={<MailOutlined />} 
                      placeholder="Enter your email"
                      style={{ borderRadius: '8px' }}
                    />
                  </Form.Item>

                  <Form.Item
                    name="password"
                    label="Password"
                    rules={[{ required: true, message: 'Please enter your password!' }]}
                  >
                    <Input.Password 
                      prefix={<LockOutlined />} 
                      placeholder="Enter your password"
                      style={{ borderRadius: '8px' }}
                    />
                  </Form.Item>

                  <Form.Item>
                    <Button 
                      type="primary" 
                      htmlType="submit" 
                      loading={loading}
                      style={{ 
                        width: '100%', 
                        height: '48px',
                        borderRadius: '8px',
                        backgroundColor: currentRole.color,
                        borderColor: currentRole.color
                      }}
                    >
                      Sign In
                    </Button>
                  </Form.Item>
                </Form>
              </TabPane>

              <TabPane 
                tab={
                  <span>
                    <UserOutlined />
                    Sign Up
                  </span>
                } 
                key="register"
              >
                <Form
                  form={registerForm}
                  onFinish={handleRegister}
                  layout="vertical"
                  size="large"
                >
                  <Form.Item
                    name="email"
                    label="Email"
                    rules={[
                      { required: true, message: 'Please enter your email!' },
                      { type: 'email', message: 'Please enter a valid email!' }
                    ]}
                  >
                    <Input 
                      prefix={<MailOutlined />} 
                      placeholder="Enter your email"
                      style={{ borderRadius: '8px' }}
                    />
                  </Form.Item>

                  <Form.Item
                    name="username"
                    label="Username"
                    rules={[{ required: true, message: 'Please enter a username!' }]}
                  >
                    <Input 
                      prefix={<UserOutlined />} 
                      placeholder="Choose a username"
                      style={{ borderRadius: '8px' }}
                    />
                  </Form.Item>

                  <Form.Item
                    name="first_name"
                    label="First Name"
                    rules={[{ required: true, message: 'Please enter your first name!' }]}
                  >
                    <Input 
                      placeholder="Enter your first name"
                      style={{ borderRadius: '8px' }}
                    />
                  </Form.Item>

                  <Form.Item
                    name="last_name"
                    label="Last Name"
                    rules={[{ required: true, message: 'Please enter your last name!' }]}
                  >
                    <Input 
                      placeholder="Enter your last name"
                      style={{ borderRadius: '8px' }}
                    />
                  </Form.Item>

                  <Form.Item
                    name="role"
                    label="Role"
                    rules={[{ required: true, message: 'Please select your role!' }]}
                  >
                    <Input 
                      disabled
                      style={{ borderRadius: '8px' }}
                    />
                  </Form.Item>

                  <Form.Item
                    name="password"
                    label="Password"
                    rules={[
                      { required: true, message: 'Please enter a password!' },
                      { min: 8, message: 'Password must be at least 8 characters!' }
                    ]}
                  >
                    <Input.Password 
                      prefix={<LockOutlined />} 
                      placeholder="Create a password"
                      style={{ borderRadius: '8px' }}
                    />
                  </Form.Item>

                  <Form.Item
                    name="password_confirm"
                    label="Confirm Password"
                    dependencies={['password']}
                    rules={[
                      { required: true, message: 'Please confirm your password!' },
                      ({ getFieldValue }) => ({
                        validator(_, value) {
                          if (!value || getFieldValue('password') === value) {
                            return Promise.resolve();
                          }
                          return Promise.reject(new Error('Passwords do not match!'));
                        },
                      }),
                    ]}
                  >
                    <Input.Password 
                      prefix={<LockOutlined />} 
                      placeholder="Confirm your password"
                      style={{ borderRadius: '8px' }}
                    />
                  </Form.Item>

                  <Form.Item>
                    <Button 
                      type="primary" 
                      htmlType="submit" 
                      loading={loading}
                      style={{ 
                        width: '100%', 
                        height: '48px',
                        borderRadius: '8px',
                        backgroundColor: currentRole.color,
                        borderColor: currentRole.color
                      }}
                    >
                      Create Account
                    </Button>
                  </Form.Item>
                </Form>
              </TabPane>
            </Tabs>

            <Divider>Or</Divider>

            <div style={{ textAlign: 'center' }}>
              <Paragraph style={{ color: '#666', marginBottom: '16px' }}>
                Need help? Contact our support team
              </Paragraph>
              <Button 
                type="link" 
                style={{ color: currentRole.color }}
                onClick={() => navigate('/')}
              >
                Back to Home
              </Button>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default LoginPage;
