import React from 'react';
import { Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

const LoadingSpinner = ({ size = 'large', text = 'Loading...' }) => {
  const antIcon = <LoadingOutlined style={{ fontSize: size === 'large' ? 24 : 16 }} spin />;

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <Spin 
        indicator={antIcon} 
        size={size}
        style={{ marginBottom: '16px' }}
      />
      <div style={{ color: 'white', fontSize: '16px' }}>
        {text}
      </div>
    </div>
  );
};

export default LoadingSpinner;
