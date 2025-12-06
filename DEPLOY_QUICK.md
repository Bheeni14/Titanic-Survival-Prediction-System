# 🚀 Quick Deploy - Vercel + Render

## Step-by-Step Deployment

### 🔧 Part 1: Push to GitHub

```cmd
cd d:\titanic
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 🖥️ Part 2: Deploy Backend to Render (5 minutes)

1. **Go to**: https://render.com → Sign up with GitHub
2. **Click**: "New +" → "Web Service"
3. **Select**: Your repository `Titanic-Survival-Prediction-Model`
4. **Configure**:
   - Name: `titanic-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: **Free**
5. **Click**: "Create Web Service"
6. **Wait**: 5-10 minutes for deployment
7. **Copy URL**: `https://titanic-api-xyz.onrender.com`

### 🎨 Part 3: Update Frontend API URL

```cmd
cd d:\titanic\frontend
```

Edit `.env` file:
```env
REACT_APP_API_URL=https://titanic-api-xyz.onrender.com
```
(Use your actual Render URL)

### 🌐 Part 4: Deploy Frontend to Vercel (2 minutes)

```cmd
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd d:\titanic\frontend
vercel --prod
```

Follow prompts:
- Project name: `titanic-survival-predictor`
- Framework: Auto-detected (Create React App)
- Build: Auto-configured

**Your app is live!** 🎉

---

## 📱 Quick Commands Reference

### Deploy Backend (via Git):
```cmd
cd d:\titanic
git add .
git commit -m "Update"
git push
```
(Render auto-deploys from GitHub)

### Deploy Frontend:
```cmd
cd d:\titanic\frontend
vercel --prod
```

### View Logs:
- **Render**: https://dashboard.render.com → Your service → Logs
- **Vercel**: https://vercel.com/dashboard → Your project → Deployments

---

## 🔗 Your Live URLs

After deployment:
- **Frontend**: `https://titanic-survival-predictor.vercel.app`
- **Backend**: `https://titanic-api-xyz.onrender.com`
- **API Docs**: `https://titanic-api-xyz.onrender.com/docs`

---

## ⚙️ Update Backend CORS (Important!)

Open `backend/main.py` and update CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://titanic-survival-predictor.vercel.app",  # Your Vercel URL
        "http://localhost:3000",  # For local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then push changes:
```cmd
git add backend/main.py
git commit -m "Update CORS for production"
git push
```

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed to Render
- [ ] Backend URL copied
- [ ] Frontend .env updated with backend URL
- [ ] Frontend deployed to Vercel
- [ ] CORS updated in backend
- [ ] Tested prediction on live site

---

## 💡 Pro Tips

1. **First load slow?** Render free tier sleeps after 15 min. First request wakes it (takes 30 sec).

2. **Keep backend awake**: Use a service like UptimeRobot to ping every 14 minutes.

3. **Custom domain**: Add in Vercel/Render dashboards (Settings → Domains).

4. **Environment variables**: Set in dashboards, not in code!

5. **Monitor**: Check Render/Vercel dashboards for errors.

---

## 🐛 Common Issues

**"API not responding":**
- Check backend URL in frontend `.env`
- Verify backend is running in Render dashboard
- Check CORS settings include Vercel URL

**"Module not found" on Render:**
- Ensure all packages in `requirements.txt`
- Check Python version is 3.11.8

**"Build failed" on Vercel:**
- Run `npm install` locally first
- Check for missing dependencies
- Try `vercel --force`

---

## 🎯 Success!

Your full-stack ML application is now deployed with:
- ✅ React frontend on Vercel (Global CDN)
- ✅ FastAPI backend on Render
- ✅ XGBoost ML model (80.45% accuracy)
- ✅ Automatic HTTPS
- ✅ Auto-deploy on git push

**Share your live app and impress everyone!** 🚢✨
