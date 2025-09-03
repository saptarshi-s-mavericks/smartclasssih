const API_BASE_URL = 'http://localhost:8000/api';

export const authService = {
  async login(credentials) {
    try {
      const response = await fetch(`${API_BASE_URL}/accounts/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });
      
      if (!response.ok) {
        throw new Error('Login failed');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      throw error;
    }
  },

  async register(userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/accounts/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
      
      if (!response.ok) {
        throw new Error('Registration failed');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      throw error;
    }
  },

  async logout() {
    try {
      const response = await fetch(`${API_BASE_URL}/accounts/logout/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      return response.ok;
    } catch (error) {
      throw error;
    }
  },

  async getCurrentUser() {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }

      const response = await fetch(`${API_BASE_URL}/accounts/profile/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error('Failed to get user profile');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      // For demo purposes, return a mock user
      return {
        id: 1,
        username: 'demo_user',
        email: 'demo@example.com',
        role: 'admin',
        firstName: 'Demo',
        lastName: 'User'
      };
    }
  },

  async updateProfile(profileData) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }

      const response = await fetch(`${API_BASE_URL}/accounts/profile/update/`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData),
      });
      
      if (!response.ok) {
        throw new Error('Failed to update profile');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      throw error;
    }
  },

  async changePassword(passwordData) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }

      const response = await fetch(`${API_BASE_URL}/accounts/change-password/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(passwordData),
      });
      
      if (!response.ok) {
        throw new Error('Failed to change password');
      }
      
      return true;
    } catch (error) {
      throw error;
    }
  },
};
