# HRMS Lite Frontend

A React frontend for the Human Resource Management System.

## Features

- Employee management interface
- Attendance tracking and visualization
- Responsive design with Tailwind CSS
- Real-time data updates
- Comprehensive error handling
- Loading and empty states

## Tech Stack

- **Framework**: React 18
- **Routing**: React Router
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **State Management**: React Hooks

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API URL
```

3. Start development server:
```bash
npm start
```

The application will be available at http://localhost:3000

## Environment Variables

- `REACT_APP_API_URL`: Backend API URL

## Project Structure

```
src/
├── components/
│   ├── Layout.jsx          # Main layout with navigation
│   ├── EmployeeForm.jsx    # Employee creation/edit form
│   ├── EmployeeList.jsx    # Employee list with actions
│   ├── AttendanceForm.jsx  # Attendance marking form
│   └── AttendanceList.jsx  # Attendance records with stats
├── services/
│   └── api.js              # API service layer
├── hooks/
│   └── useApi.js           # Custom hooks for API calls
├── App.jsx                 # Main application component
└── main.jsx               # Application entry point
```

## Features

### Dashboard
- Overview statistics
- Quick access to main functions

### Employee Management
- Add new employees with validation
- View all employees in a table
- Edit employee information
- Delete employees with confirmation

### Attendance Tracking
- Mark attendance for employees
- View attendance records with filtering
- Attendance statistics and percentages
- Date range filtering

## Deployment

### Vercel (Recommended)
1. Connect your GitHub repository
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push

### Netlify
1. Connect your GitHub repository
2. Configure build settings
3. Set environment variables
4. Deploy

## Build for Production

```bash
npm run build
```

This creates an optimized build in the `build` folder ready for deployment.
