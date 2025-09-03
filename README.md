# Campus Ecosystem - Integrated Digital Platform 🏫

A comprehensive digital platform that transforms campus management through intelligent scheduling, role-based portals, and AI-powered support systems.

## 🌟 Features

### Core Components
- **Intelligent Timetable Generator** - Advanced constraint satisfaction & optimization
- **Multi-User Role System** - Admin, Faculty, Student, and Parent portals
- **Smart Q&A Desk** - AI-powered support using Google Gemini API
- **Attendance Management** - Real-time tracking and analytics
- **Academic Performance Monitoring** - Marks, attendance, and progress tracking

### User Portals
- **Administrator Portal** - Full system control and analytics
- **Faculty Portal** - Schedule management and student interaction
- **Student Portal** - Personal academic dashboard
- **Parent Portal** - Child progress monitoring

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** with Django 4.2
- **PostgreSQL** database
- **Google OR-Tools** for scheduling optimization
- **Google Gemini API** for AI-powered Q&A
- **Django REST Framework** for APIs

### Frontend
- **React.js** with Ant Design
- **Chart.js** for analytics visualization
- **Responsive design** for all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis (for Celery tasks)

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm start
```

## 📁 Project Structure

```
campus-ecosystem/
├── backend/                 # Django backend
│   ├── campus_ecosystem/   # Main Django project
│   ├── accounts/           # User management
│   ├── scheduling/         # Timetable generation
│   ├── attendance/         # Attendance tracking
│   ├── academics/          # Marks and performance
│   └── qa_system/          # AI Q&A system
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   └── public/             # Static files
├── requirements.txt         # Python dependencies
├── package.json            # Node.js dependencies
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/campus_ecosystem
GOOGLE_GEMINI_API_KEY=your-gemini-api-key
REDIS_URL=redis://localhost:6379
```

### Database Setup
1. Create PostgreSQL database
2. Update `.env` with database credentials
3. Run migrations: `python manage.py migrate`

## 🎯 Development Phases

1. **Phase 1**: Foundation - User Management & Data Modeling
2. **Phase 2**: Core Scheduling Engine
3. **Phase 3**: User Portals (UI/UX)
4. **Phase 4**: Smart Features Integration

## 🏆 Unique Selling Points

- **360° Campus Solution** - Single source of truth for all stakeholders
- **Data-Driven Insights** - Proactive identification of at-risk students
- **AI-Powered Support** - 24/7 automated assistance
- **Enhanced Parental Engagement** - Real-time progress monitoring
- **NEP 2020 Compliant** - Advanced scheduling for modern education

## 📞 Support

For technical support or questions, please refer to the documentation or contact the development team.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
