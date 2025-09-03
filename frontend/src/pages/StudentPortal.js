import React from 'react';
import { Card, Row, Col, Statistic, Button, Space } from 'antd';
import { BookOutlined, CalendarOutlined, TrophyOutlined, UserOutlined } from '@ant-design/icons';

const StudentPortal = () => {
  return (
    <div style={{ padding: '24px' }}>
      <h1>Student Portal</h1>
      
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic title="My Subjects" value={6} prefix={<BookOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Today's Classes" value={4} prefix={<CalendarOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Attendance" value="88%" prefix={<UserOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="CGPA" value="8.5" prefix={<TrophyOutlined />} />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="Today's Schedule">
            <p>9:00 AM - Mathematics 101</p>
            <p>10:30 AM - Physics Lab</p>
            <p>2:00 PM - English</p>
            <p>4:00 PM - Computer Science</p>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Quick Actions">
            <Space direction="vertical" style={{ width: '100%' }}>
              <Button type="primary" block>View Timetable</Button>
              <Button block>Check Attendance</Button>
              <Button block>View Marks</Button>
              <Button block>Download Assignments</Button>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default StudentPortal;
