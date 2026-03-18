# HRMS Lite Deployment Guide

This guide provides step-by-step instructions for deploying the HRMS Lite application to production.

## 📋 Prerequisites

- GitHub account with repository
- Render account (for backend)
- Vercel account (for frontend)
- Code pushed to GitHub repository

## 🚀 Step 1: GitHub Setup

### Initialize Repository (if not done)
```bash
# Navigate to project root
cd c:\project\hrms

# Initialize git repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: HRMS Lite full-stack application with authentication"

# Create main branch
git branch -M main

# Add remote origin (replace with your GitHub repo)
git remote add origin https://github.com/yourusername/hrms-lite.git

# Push to GitHub
git push -u origin main
```

### Verify .gitignore
Ensure your `.gitignore` file includes:
- `node_modules/`
- `__pycache__/`
- `*.env`
- `frontend/build/`
- `*.db`

## 🐍 Step 2: Backend Deployment (Render)

### 2.1 Prepare Backend
```bash
# Ensure requirements.txt includes psycopg2-binary
pip install psycopg2-binary==2.9.7
pip freeze > requirements.txt
```

### 2.2 Deploy to Render
1. **Go to [render.com](https://render.com)**
2. **Sign up/login** with GitHub
3. **Click "New+" → "Web Service"**
4. **Connect Repository**: Select your GitHub repo
5. **Configure Service**:
   - **Name**: `hrms-lite-api`
   - **Environment**: `Python 3`
   - **Branch**: `main`
   - **Root Directory**: `backend`

### 2.3 Build & Start Commands
```yaml
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 2.4 Environment Variables
Add these in Render dashboard:
```env
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-super-secret-jwt-key-here
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
```

### 2.5 Database Setup
1. **Create PostgreSQL Database**:
   - In Render dashboard: "New+" → "PostgreSQL"
   - Name: `hrms-db`
   - Wait for database to be ready

2. **Get Database URL**:
   - Go to database page
   - Copy "Connection" URL
   - Add to environment variables

### 2.6 Deploy
- Click "Create Web Service"
- Wait for deployment to complete
- Test API: `https://your-app-name.onrender.com/health`

## ⚛️ Step 3: Frontend Deployment (Vercel)

### 3.1 Prepare Frontend
```bash
# Ensure vercel.json exists in project root
# It should be configured for frontend build
```

### 3.2 Deploy to Vercel
1. **Go to [vercel.com](https://vercel.com)**
2. **Sign up/login** with GitHub
3. **Click "New Project"**
4. **Import Repository**: Select your GitHub repo
5. **Configure Project**:
   - **Framework Preset**: `React`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### 3.3 Environment Variables
Add in Vercel dashboard:
```env
REACT_APP_API_URL=https://your-backend-name.onrender.com
```

### 3.4 Deploy
- Click "Deploy"
- Wait for deployment to complete
- Test frontend: `https://your-project-name.vercel.app`

## 🔧 Step 4: Integration & Testing

### 4.1 Test API Endpoints
```bash
# Test backend health
curl https://your-backend.onrender.com/health

# Test authentication
curl -X POST https://your-backend.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### 4.2 Test Frontend Integration
1. Open your Vercel frontend URL
2. Try to register a new user
3. Login with credentials
4. Test employee management
5. Test attendance tracking

### 4.3 Common Issues & Fixes

#### CORS Issues
**Problem**: Frontend can't connect to backend
**Solution**: Update `ALLOWED_ORIGINS` in backend environment variables
```env
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

#### Database Connection Issues
**Problem**: Backend can't connect to database
**Solution**: Verify `DATABASE_URL` format
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
```

#### Environment Variables Missing
**Problem**: App crashes or authentication fails
**Solution**: Check all required environment variables are set

#### Backend Sleep (Render Free Tier)
**Problem**: API responses are slow after inactivity
**Solution**: Render free tier sleeps after 15 minutes - this is normal

## 📝 Step 5: Final Configuration

### Update README.md
Replace placeholder URLs with your actual URLs:
```markdown
## 🌐 Live Demo

- **Frontend**: https://your-project-name.vercel.app
- **Backend API**: https://your-backend-name.onrender.com
- **API Documentation**: https://your-backend-name.onrender.com/docs
```

### Test Complete Flow
1. **User Registration**: Create new account
2. **User Login**: Authenticate with credentials
3. **Employee Management**: Add/view/delete employees
4. **Attendance Tracking**: Mark and view attendance
5. **Statistics**: Check attendance reports

## 🚨 Troubleshooting

### Backend Issues
```bash
# Check Render logs
- Go to your service on Render.com
- Click "Logs" tab
- Look for error messages

# Common fixes:
- Restart service
- Check environment variables
- Verify database connection
```

### Frontend Issues
```bash
# Check Vercel logs
- Go to your project on Vercel.com
- Click "Logs" tab
- Look for build or runtime errors

# Common fixes:
- Redeploy project
- Check environment variables
- Verify API URL
```

### Integration Issues
1. **Clear browser cache and localStorage**
2. **Check network tab in browser dev tools**
3. **Verify CORS configuration**
4. **Test API endpoints directly**

## 🎯 Success Checklist

- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] Database connected and working
- [ ] User registration works
- [ ] User login works
- [ ] Employee management works
- [ ] Attendance tracking works
- [ ] No CORS errors
- [ ] Environment variables configured
- [ ] README.md updated with live URLs

## 📞 Support

If you encounter issues:
1. Check Render and Vercel logs
2. Review environment variables
3. Test API endpoints directly
4. Check this troubleshooting guide
5. Open an issue on GitHub

---

**Congratulations!** Your HRMS Lite application is now deployed and ready for production use.
