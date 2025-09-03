import React from 'react';
import { Card, Row, Col, Statistic, Button, Table, Space } from 'antd';
import { UserOutlined, CalendarOutlined, BarChartOutlined, SettingOutlined } from '@ant-design/icons';

const AdminPortal = () => {
  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Role',
      dataIndex: 'role',
      key: 'role',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Button type="primary" size="small">Edit</Button>
          <Button size="small">Delete</Button>
        </Space>
      ),
    },
  ];

  const data = [
    {
      key: '1',
      name: 'John Doe',
      role: 'Faculty',
      status: 'Active',
    },
    {
      key: '2',
      name: 'Jane Smith',
      role: 'Student',
      status: 'Active',
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <h1>Admin Portal</h1>
      
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Users"
              value={1128}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Active Timetables"
              value={15}
              prefix={<CalendarOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Departments"
              value={8}
              prefix={<BarChartOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="System Status"
              value="Online"
              prefix={<SettingOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="User Management" style={{ marginBottom: '16px' }}>
            <Button type="primary" style={{ marginBottom: '16px' }}>
              Add New User
            </Button>
            <Table columns={columns} dataSource={data} size="small" />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Quick Actions">
            <Space direction="vertical" style={{ width: '100%' }}>
              <Button type="primary" block>Generate Timetable</Button>
              <Button block>View Reports</Button>
              <Button block>System Settings</Button>
              <Button block>Backup Database</Button>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default AdminPortal;
