import React from 'react';
import { Card, Row, Col, Statistic, Button, Table, Space } from 'antd';
import { BookOutlined, CalendarOutlined, UserOutlined, TrophyOutlined } from '@ant-design/icons';

const FacultyPortal = () => {
  return (
    <div style={{ padding: '24px' }}>
      <h1>Faculty Portal</h1>
      
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic title="My Classes" value={5} prefix={<BookOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Today's Classes" value={3} prefix={<CalendarOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Total Students" value={120} prefix={<UserOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Attendance Rate" value="92%" prefix={<TrophyOutlined />} />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="Today's Schedule">
            <p>9:00 AM - Mathematics 101</p>
            <p>11:00 AM - Advanced Calculus</p>
            <p>2:00 PM - Statistics Lab</p>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Quick Actions">
            <Space direction="vertical" style={{ width: '100%' }}>
              <Button type="primary" block>Mark Attendance</Button>
              <Button block>Upload Marks</Button>
              <Button block>View Timetable</Button>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default FacultyPortal;
