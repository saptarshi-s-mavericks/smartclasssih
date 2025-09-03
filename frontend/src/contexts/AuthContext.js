import React, { createContext, useContext, useState, useEffect } from 'react';
import { message } from 'antd';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      try {
        if (token) {
          const userData = await authService.getCurrentUser();
          setUser(userData);
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
        setToken(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [token]);

  // Login function
  const login = async (credentials) => {
    try {
      setLoading(true);
      const response = await authService.login(credentials);
      
      if (response.user && response.token) {
        setUser(response.user);
        setToken(response.token);
        localStorage.setItem('token', response.token);
        message.success('Login successful!');
        return { success: true };
      } else {
        message.error('Login failed. Please check your credentials.');
        return { success: false, error: 'Invalid response from server' };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Login failed. Please try again.';
      message.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setToken(null);
      localStorage.removeItem('token');
      message.success('Logged out successfully');
    }
  };

  // Register function
  const register = async (userData) => {
    try {
      setLoading(true);
      const response = await authService.register(userData);
      
      if (response.user) {
        message.success('Registration successful! Please log in.');
        return { success: true };
      } else {
        message.error('Registration failed. Please try again.');
        return { success: false, error: 'Invalid response from server' };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Registration failed. Please try again.';
      message.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  // Update user profile
  const updateProfile = async (profileData) => {
    try {
      setLoading(true);
      const updatedUser = await authService.updateProfile(profileData);
      setUser(updatedUser);
      message.success('Profile updated successfully!');
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Profile update failed. Please try again.';
      message.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  // Change password
  const changePassword = async (passwordData) => {
    try {
      setLoading(true);
      await authService.changePassword(passwordData);
      message.success('Password changed successfully!');
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Password change failed. Please try again.';
      message.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  // Check if user has specific role
  const hasRole = (role) => {
    return user && user.role === role;
  };

  // Check if user has any of the specified roles
  const hasAnyRole = (roles) => {
    return user && roles.includes(user.role);
  };

  // Check if user is admin
  const isAdmin = () => hasRole('admin');

  // Check if user is faculty
  const isFaculty = () => hasRole('faculty');

  // Check if user is student
  const isStudent = () => hasRole('student');

  // Check if user is parent
  const isParent = () => hasRole('parent');

  const value = {
    user,
    loading,
    token,
    login,
    logout,
    register,
    updateProfile,
    changePassword,
    hasRole,
    hasAnyRole,
    isAdmin,
    isFaculty,
    isStudent,
    isParent,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
