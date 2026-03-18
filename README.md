# HRMS Lite - Human Resource Management System

A lightweight, production-ready HR management system with employee records and attendance tracking.

## 🚀 Features

### Core Features
- **User Authentication**: JWT-based login/registration system
- **Employee Management**: Add, view, edit, and delete employee records
- **Attendance Tracking**: Mark daily attendance with statistics
- **Professional UI**: Clean, responsive design with Tailwind CSS
- **Real-time Updates**: Automatic data refresh and state management

### Bonus Features
- **Dashboard**: Overview statistics and quick navigation
- **Attendance Statistics**: Total days, present days, absent days, attendance percentage
- **Date Filtering**: Filter attendance records by date range
- **Error Handling**: Comprehensive error messages and loading states

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL ORM and toolkit
- **Pydantic** - Data validation using Python type hints
- **JWT** - Authentication tokens
- **PostgreSQL** - Production database

## 📁 Project Structure

```
hrms/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── utils/        # Authentication utilities
│   │   └── main.py       # FastAPI application
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API service layer
│   │   └── App.jsx       # Main application
│   ├── package.json
│   └── README.md
├── vercel.json           # Vercel configuration
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🌐 Live Demo

- **Frontend**: https://hrms-lite.vercel.app
- **Backend API**: https://hrms-lite-api.onrender.com
- **API Documentation**: https://hrms-lite-api.onrender.com/docs

## 🚀 Quick Start

### Local Development

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/hrms-lite.git
cd hrms-lite
```

2. **Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. **Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API URL

# Start the frontend development server
npm start
```

4. **Access Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔧 Configuration

### Backend Environment Variables
```env
DATABASE_URL=sqlite:///./hrms.db
SECRET_KEY=your-super-secret-jwt-key
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.vercel.app
```

### Frontend Environment Variables
```env
REACT_APP_API_URL=http://localhost:8000  # Development
REACT_APP_API_URL=https://your-api.onrender.com  # Production
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Employees
- `GET /api/employees` - Get all employees
- `POST /api/employees` - Create employee
- `DELETE /api/employees/{employee_id}` - Delete employee
- `GET /api/employees/next-id` - Get next employee ID

### Attendance
- `POST /api/attendance` - Mark attendance
- `GET /api/attendance/{employee_id}` - Get attendance records
- `GET /api/attendance/{employee_id}/stats` - Get attendance statistics

## 🚀 Deployment

### Backend (Render)
1. **Connect Repository**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Create new "Web Service"

2. **Configuration**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     ```
     DATABASE_URL=postgresql://username:password@host:port/database
     SECRET_KEY=your-super-secret-jwt-key
     ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
     ```

3. **Database Setup**
   - Add PostgreSQL database in Render
   - Copy DATABASE_URL to environment variables

### Frontend (Vercel)
1. **Connect Repository**
   - Go to [vercel.com](https://vercel.com)
   - Connect your GitHub repository
   - Import project

2. **Configuration**
   - **Framework Preset**: React
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/build`
   - **Environment Variables**:
     ```
     REACT_APP_API_URL=https://your-backend-domain.onrender.com
     ```

## 🔒 Security Features

- JWT token authentication with 24-hour expiry
- Password hashing with bcrypt
- CORS protection
- Input validation and sanitization
- SQL injection prevention through SQLAlchemy ORM

## 🐛 Common Issues & Solutions

### Backend Issues
1. **CORS Errors**: Update `ALLOWED_ORIGINS` in backend environment variables
2. **Database Connection**: Verify `DATABASE_URL` format and credentials
3. **Missing SECRET_KEY**: Set a strong JWT secret in environment variables

### Frontend Issues
1. **API Connection Errors**: Check `REACT_APP_API_URL` environment variable
2. **Build Failures**: Ensure all dependencies are installed
3. **Authentication Issues**: Clear localStorage and re-login

### Integration Issues
1. **Backend Sleep**: Render free tier sleeps after 15 minutes inactivity
2. **Token Expiry**: JWT tokens expire after 24 hours
3. **Network Errors**: Check CORS configuration and API endpoints

## 📝 Assumptions

- Single user system (no role-based access control)
- Email validation without email verification
- JWT tokens expire after 24 hours
- PostgreSQL for production, SQLite for development
- No refresh token implementation (simplified auth)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Open an issue in the GitHub repository
- Check the [API Documentation](https://hrms-lite-api.onrender.com/docs)
- Review the troubleshooting section above

---

**HRMS Lite** - Simple, efficient, and production-ready HR management system.
