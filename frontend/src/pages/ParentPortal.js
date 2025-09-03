import React from 'react';
import { Card, Row, Col, Statistic, Button, Space } from 'antd';
import { UserOutlined, BookOutlined, TrophyOutlined, CalendarOutlined } from '@ant-design/icons';

const ParentPortal = () => {
  return (
    <div style={{ padding: '24px' }}>
      <h1>Parent Portal</h1>
      
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic title="Child's Name" value="John Smith" prefix={<UserOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Class" value="12th Grade" prefix={<BookOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Attendance" value="92%" prefix={<CalendarOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="CGPA" value="8.7" prefix={<TrophyOutlined />} />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="Recent Performance">
            <p>Mathematics: A+ (95%)</p>
            <p>Physics: A (88%)</p>
            <p>English: A- (85%)</p>
            <p>Computer Science: A+ (92%)</p>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Quick Actions">
            <Space direction="vertical" style={{ width: '100%' }}>
              <Button type="primary" block>View Progress Report</Button>
              <Button block>Check Attendance</Button>
              <Button block>View Timetable</Button>
              <Button block>Contact Teachers</Button>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default ParentPortal;
