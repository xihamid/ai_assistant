# 🚀 Free Deployment Guide for Personalized Research Assistant

## 📋 Overview
This guide shows you how to deploy your Personalized Research Assistant API for FREE using various cloud platforms.

## 🎯 Prerequisites
- GitHub account
- API Keys (OpenAI & Tavily)
- Basic understanding of deployment

---

## 🌟 Option 1: Railway (Recommended - Easiest)

### Step 1: Prepare Your Project
1. Create a `Procfile` in your project root:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Create `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
```

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `TAVILY_API_KEY`: Your Tavily API key
6. Deploy!

**Free Tier**: $5 credit monthly, 500 hours runtime

---

## 🌟 Option 2: Render (Popular Choice)

### Step 1: Prepare Your Project
1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: research-assistant
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: TAVILY_API_KEY
        sync: false
```

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Add environment variables in dashboard
6. Deploy!

**Free Tier**: 750 hours/month, sleeps after 15 minutes of inactivity

---

## 🌟 Option 3: Heroku (Classic Choice)

### Step 1: Prepare Your Project
1. Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Create `runtime.txt`:
```
python-3.11.0
```

### Step 2: Deploy to Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variables:
   ```bash
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set TAVILY_API_KEY=your_key
   ```
5. Deploy: `git push heroku main`

**Free Tier**: No longer available (paid plans only)

---

## 🌟 Option 4: PythonAnywhere (Simple)

### Step 1: Prepare Your Project
1. Upload your code to PythonAnywhere
2. Install dependencies in Bash console:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

### Step 2: Configure Web App
1. Go to Web tab
2. Create new web app
3. Choose "Manual configuration"
4. Set Python version to 3.10
5. Add environment variables in Web tab
6. Configure WSGI file

**Free Tier**: Limited CPU seconds, single web app

---

## 🌟 Option 5: Fly.io (Modern)

### Step 1: Prepare Your Project
1. Create `fly.toml`:
```toml
app = "your-app-name"
primary_region = "iad"

[build]

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### Step 2: Deploy to Fly.io
1. Install Fly CLI
2. Login: `fly auth login`
3. Launch: `fly launch`
4. Set secrets:
   ```bash
   fly secrets set OPENAI_API_KEY=your_key
   fly secrets set TAVILY_API_KEY=your_key
   ```
5. Deploy: `fly deploy`

**Free Tier**: 3 shared-cpu-1x 256mb VMs, 160GB-hours/month

---

## 🔧 Environment Variables Setup

### Required Environment Variables:
```bash
OPENAI_API_KEY=sk-proj-your-openai-key-here
TAVILY_API_KEY=tvly-your-tavily-key-here
```

### Optional Environment Variables:
```bash
SECRET_KEY=your-jwt-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 📝 Pre-Deployment Checklist

### ✅ Code Preparation:
- [ ] All dependencies in `requirements.txt`
- [ ] No hardcoded API keys in code
- [ ] Database file (SQLite) will be created automatically
- [ ] All imports working correctly
- [ ] FastAPI app runs locally

### ✅ Security:
- [ ] API keys in environment variables
- [ ] JWT secret key is secure
- [ ] No sensitive data in code
- [ ] CORS configured if needed

### ✅ Performance:
- [ ] Database queries optimized
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Health check endpoint working

---

## 🚀 Quick Start Commands

### For Railway:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### For Render:
```bash
# Just push to GitHub, Render auto-deploys
git add .
git commit -m "Deploy to Render"
git push origin main
```

### For Fly.io:
```bash
# Install and deploy
curl -L https://fly.io/install.sh | sh
fly launch
fly deploy
```

---

## 🔍 Testing Your Deployment

### 1. Health Check:
```bash
curl https://your-app-url.railway.app/
```

### 2. Register User:
```bash
curl -X POST https://your-app-url.railway.app/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User",
    "summary_length": "short"
  }'
```

### 3. Login:
```bash
curl -X POST https://your-app-url.railway.app/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

---

## 💡 Pro Tips

### 1. Database Considerations:
- SQLite files are ephemeral on most free tiers
- Consider upgrading to PostgreSQL for production
- Implement database backups

### 2. Performance Optimization:
- Use connection pooling
- Implement caching
- Optimize API responses
- Monitor resource usage

### 3. Monitoring:
- Set up health checks
- Monitor API usage
- Track error rates
- Set up alerts

### 4. Security:
- Use HTTPS (most platforms provide this)
- Implement rate limiting
- Validate all inputs
- Use secure headers

---

## 🆘 Troubleshooting

### Common Issues:

**1. App Won't Start:**
- Check `requirements.txt` has all dependencies
- Verify environment variables are set
- Check logs for import errors

**2. Database Issues:**
- SQLite file permissions
- Database path issues
- Connection timeouts

**3. API Key Issues:**
- Verify keys are correctly set
- Check key permissions
- Ensure no extra spaces in keys

**4. Memory Issues:**
- Optimize code
- Reduce dependencies
- Use smaller base images

---

## 📊 Platform Comparison

| Platform | Free Tier | Ease of Use | Performance | Best For |
|----------|-----------|-------------|-------------|----------|
| Railway | $5 credit | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Beginners |
| Render | 750 hrs | ⭐⭐⭐⭐ | ⭐⭐⭐ | Production |
| Fly.io | 160GB-hrs | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Advanced |
| PythonAnywhere | Limited | ⭐⭐⭐⭐⭐ | ⭐⭐ | Simple apps |

---

## 🎯 Recommended Deployment Flow

1. **Start with Railway** (easiest)
2. **Test thoroughly** with your APIs
3. **Monitor usage** and performance
4. **Upgrade to paid plan** if needed
5. **Consider Render** for production

---

## 📞 Support

- **Railway**: [docs.railway.app](https://docs.railway.app)
- **Render**: [render.com/docs](https://render.com/docs)
- **Fly.io**: [fly.io/docs](https://fly.io/docs)
- **PythonAnywhere**: [help.pythonanywhere.com](https://help.pythonanywhere.com)

---

**Happy Deploying! 🚀**

*Last updated: October 2024*
