# Campus Ecosystem - Project Structure 📁

## Overview
This document provides a comprehensive overview of the Campus Ecosystem project structure, explaining the organization of both backend and frontend components.

## Root Directory Structure
```
campus-ecosystem/
├── README.md                    # Main project documentation
├── PROJECT_STRUCTURE.md         # This file - detailed structure overview
├── requirements.txt             # Python backend dependencies
├── package.json                # Node.js frontend dependencies
├── setup.py                    # Automated setup script
├── backend/                    # Django backend application
├── frontend/                   # React frontend application
└── docs/                       # Additional documentation
```

## Backend Structure (Django) 🐍

### Core Django Project
```
backend/
├── manage.py                   # Django management script
├── campus_ecosystem/          # Main Django project settings
│   ├── __init__.py
│   ├── settings.py            # Django settings and configuration
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI application entry point
│   └── asgi.py                # ASGI application entry point
├── .env                       # Environment variables (created from env_example.txt)
└── env_example.txt            # Environment configuration template
```

### Django Applications

#### 1. Accounts App (`backend/accounts/`)
**Purpose**: User management, authentication, and role-based access control

**Key Models**:
- `User`: Custom user model with role-based permissions
- `Department`: Academic departments
- `FacultyProfile`: Extended faculty information
- `StudentProfile`: Extended student information
- `ParentProfile`: Extended parent information
- `ParentStudentRelationship`: Links parents to students
- `Invitation`: Email invitations for new users

**Key Features**:
- Role-based authentication (Admin, Faculty, Student, Parent)
- Email invitation system
- Profile management
- Department management

#### 2. Scheduling App (`backend/scheduling/`)
**Purpose**: Core timetable generation and scheduling management

**Key Models**:
- `Subject`: Academic subjects/courses
- `Room`: Classrooms and facilities
- `TimeSlot`: Available time slots
- `ClassSchedule`: Individual class sessions
- `StudentGroup`: Groups of students (classes, sections)
- `Timetable`: Generated timetables
- `SchedulingConstraint`: Constraints for optimization
- `FacultyAvailability`: Faculty availability tracking

**Key Features**:
- Intelligent timetable generation using Google OR-Tools
- Constraint satisfaction and optimization
- Room allocation and conflict resolution
- Faculty availability management

#### 3. Attendance App (`backend/attendance/`)
**Purpose**: Student attendance tracking and management

**Key Models**:
- `Attendance`: Individual attendance records
- `AttendanceSession`: Attendance marking sessions
- `AttendanceReport`: Generated attendance reports
- `AttendancePolicy`: Attendance rules and policies
- `AttendanceAlert`: Low attendance alerts
- `AttendanceStatistics`: Pre-calculated statistics

**Key Features**:
- Real-time attendance tracking
- Bulk attendance marking
- Automated alerts for low attendance
- Comprehensive reporting system

#### 4. Academics App (`backend/academics/`)
**Purpose**: Academic performance tracking and management

**Key Models**:
- `Exam`: Examination definitions
- `ExamResult`: Individual student results
- `Grade`: Grade definitions and scales
- `SubjectGrade`: Final subject grades
- `AcademicPerformance`: Overall performance metrics
- `Assignment`: Academic assignments
- `AcademicCalendar`: Academic events and calendar

**Key Features**:
- Comprehensive exam management
- Grade calculation and tracking
- Performance analytics
- Assignment management

#### 5. Q&A System App (`backend/qa_system/`)
**Purpose**: AI-powered support system using Google Gemini

**Key Models**:
- `KnowledgeBase`: FAQ and knowledge articles
- `ChatSession`: Chat sessions with AI
- `ChatMessage`: Individual chat messages
- `AIResponse`: AI-generated responses
- `SupportTicket`: Support ticket system
- `AIConfiguration`: AI behavior configuration

**Key Features**:
- Smart Q&A with Google Gemini integration
- Knowledge base management
- Chat session tracking
- Support ticket system

## Frontend Structure (React) ⚛️

### Core Application Files
```
frontend/
├── public/
│   ├── index.html             # Main HTML template
│   ├── favicon.ico            # Application icon
│   └── manifest.json          # PWA manifest
├── src/
│   ├── index.js               # Application entry point
│   ├── index.css              # Global CSS styles
│   ├── App.js                 # Main application component
│   ├── App.css                # Application-specific styles
│   ├── contexts/              # React contexts
│   ├── components/            # Reusable components
│   ├── pages/                 # Page components
│   ├── services/              # API services
│   └── utils/                 # Utility functions
└── package.json               # Dependencies and scripts
```

### React Contexts (`frontend/src/contexts/`)
- `AuthContext.js`: Authentication state management
- `ThemeContext.js`: Theme and styling management

### Components (`frontend/src/components/`)
- `common/`: Shared components (LoadingSpinner, etc.)
- `SmartQAChat.js`: AI-powered chat interface

### Pages (`frontend/src/pages/`)
- `LandingPage.js`: Public landing page
- `LoginPage.js`: Authentication page
- `Dashboard.js`: Main dashboard
- `AdminPortal.js`: Administrator portal
- `FacultyPortal.js`: Faculty portal
- `StudentPortal.js`: Student portal
- `ParentPortal.js`: Parent portal

## Key Features by User Role 👥

### Administrator Portal
- **User Management**: Create, edit, and manage all user accounts
- **Timetable Generation**: Configure and run the intelligent scheduler
- **System Analytics**: View comprehensive system statistics
- **Configuration**: Manage departments, subjects, and system settings

### Faculty Portal
- **Personal Schedule**: View assigned classes and schedule
- **Attendance Management**: Mark and track student attendance
- **Student Performance**: Monitor student progress and grades
- **Assignment Management**: Create and grade assignments

### Student Portal
- **My Timetable**: View personal class schedule
- **Attendance Tracking**: Monitor personal attendance records
- **Performance Metrics**: View grades and academic progress
- **Assignment Submissions**: Submit and track assignments

### Parent Portal
- **Child Progress**: Monitor child's academic performance
- **Attendance Reports**: View child's attendance records
- **Performance Tracking**: Track grades and achievements
- **Communication**: Access to academic calendar and updates

## Technology Stack 🛠️

### Backend
- **Framework**: Django 4.2 with Django REST Framework
- **Database**: PostgreSQL
- **Optimization**: Google OR-Tools for scheduling
- **AI Integration**: Google Gemini API
- **Task Queue**: Celery with Redis
- **Authentication**: Custom role-based system

### Frontend
- **Framework**: React 18 with React Router
- **UI Library**: Ant Design
- **Styling**: CSS with responsive design
- **State Management**: React Context API
- **HTTP Client**: Axios for API communication

### Development Tools
- **Package Manager**: pip (Python), npm (Node.js)
- **Version Control**: Git
- **Environment**: Virtual environments for Python
- **Setup**: Automated setup script (setup.py)

## Database Schema 🗄️

### Core Relationships
1. **Users** → **Profiles** (One-to-One)
2. **Departments** → **Subjects** (One-to-Many)
3. **Subjects** → **Classes** (One-to-Many)
4. **Students** → **Groups** (Many-to-Many)
5. **Parents** → **Students** (Many-to-Many through relationships)
6. **Classes** → **Attendance** (One-to-Many)
7. **Exams** → **Results** (One-to-Many)

### Key Constraints
- Unique email addresses for users
- Unique student/faculty IDs
- No scheduling conflicts (room, time, faculty)
- Referential integrity across all relationships

## API Structure 🌐

### Authentication Endpoints
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/logout/` - User logout
- `POST /api/accounts/register/` - User registration

### User Management
- `GET /api/accounts/profile/` - Get user profile
- `PUT /api/accounts/profile/update/` - Update profile
- `POST /api/accounts/password-change/` - Change password

### Scheduling
- `GET /api/scheduling/timetables/` - List timetables
- `POST /api/scheduling/generate/` - Generate new timetable
- `GET /api/scheduling/constraints/` - List scheduling constraints

### Attendance
- `GET /api/attendance/records/` - Get attendance records
- `POST /api/attendance/mark/` - Mark attendance
- `GET /api/attendance/reports/` - Generate reports

### Academics
- `GET /api/academics/exams/` - List exams
- `POST /api/academics/results/` - Submit exam results
- `GET /api/academics/performance/` - Get performance data

### Q&A System
- `POST /api/qa/chat/` - Send message to AI
- `GET /api/qa/knowledge/` - Get knowledge base articles
- `POST /api/qa/tickets/` - Create support tickets

## Security Features 🔒

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- Session management
- Password hashing and validation

### Data Protection
- CSRF protection
- SQL injection prevention
- XSS protection
- Input validation and sanitization

### API Security
- Rate limiting
- Request validation
- Secure headers
- CORS configuration

## Performance Optimizations ⚡

### Backend
- Database query optimization
- Caching strategies
- Async task processing
- Connection pooling

### Frontend
- Code splitting and lazy loading
- Image optimization
- Bundle size optimization
- Progressive Web App features

## Deployment Considerations 🚀

### Environment Variables
- Database credentials
- API keys (Google Gemini)
- Email configuration
- Redis connection
- Secret keys

### Infrastructure
- PostgreSQL database server
- Redis server for caching
- Web server (Nginx/Apache)
- Application server (Gunicorn/uWSGI)

### Monitoring
- Application logging
- Error tracking
- Performance monitoring
- Health checks

## Development Workflow 🔄

### Setup Process
1. Clone repository
2. Run `python setup.py` for automated setup
3. Configure environment variables
4. Set up PostgreSQL database
5. Run migrations
6. Create superuser
7. Start development servers

### Development Commands
```bash
# Backend
python backend/manage.py runserver
python backend/manage.py makemigrations
python backend/manage.py migrate

# Frontend
cd frontend
npm start
npm run build
npm test
```

### Testing Strategy
- Unit tests for models and views
- Integration tests for API endpoints
- Frontend component testing
- End-to-end testing

## Future Enhancements 🚀

### Planned Features
- Mobile application
- Advanced analytics dashboard
- Integration with external systems
- Multi-language support
- Advanced reporting tools

### Scalability Improvements
- Microservices architecture
- Load balancing
- Database sharding
- CDN integration
- Container orchestration

## Support and Documentation 📚

### Documentation
- API documentation (Swagger/OpenAPI)
- User guides for each role
- Developer documentation
- Deployment guides

### Support Channels
- Issue tracking (GitHub Issues)
- Documentation wiki
- Community forums
- Technical support

---

This structure provides a solid foundation for a comprehensive campus management system that can scale with institutional needs while maintaining code quality and developer productivity.
