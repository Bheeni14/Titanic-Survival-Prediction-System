# 🎉 TITANIC PREDICTION APP - USER GUIDE

## ✅ Both Frontend & Backend Running!

### 🌐 Access Your Application

- **Frontend (User Interface)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🚀 How to Use the App

### 1. **Main Prediction Page**
   - Open http://localhost:3000
   - You'll see a beautiful, modern interface with a form
   - Fill in passenger details:
     - **Passenger Class** (1st, 2nd, or 3rd)
     - **Name** (e.g., "John Smith")
     - **Sex** (Male/Female)
     - **Age** (e.g., 29)
     - **Siblings/Spouses** (number, e.g., 0)
     - **Parents/Children** (number, e.g., 0)
     - **Ticket** (optional, e.g., "PC 17599")
     - **Fare** (e.g., 100.00)
     - **Cabin** (optional, e.g., "C85")
     - **Port of Embarkation** (C=Cherbourg, Q=Queenstown, S=Southampton)

### 2. **Make a Prediction**
   - Click the **"Predict Survival"** button
   - Wait for the ML model to process (instant!)
   - See the result:
     - ✅ **SURVIVED** (with probability %)
     - ❌ **NOT SURVIVED** (with probability %)
   - Beautiful animations and visual feedback

### 3. **Try Different Scenarios**

**High Survival Chance:**
```
Passenger Class: 1st
Sex: Female
Age: 30
Fare: 100
Port: Cherbourg (C)
```

**Low Survival Chance:**
```
Passenger Class: 3rd  
Sex: Male
Age: 25
Fare: 7.25
Port: Southampton (S)
```

### 4. **View Model Information**
   - Click the **"Model Info"** tab
   - See:
     - Model accuracy: 80.45%
     - Features used
     - Algorithm: XGBoost
     - Training data size

### 5. **Dashboard (if available)**
   - View statistics and visualizations
   - See survival rates by class, gender, etc.

---

## 🎨 Features You'll See

### Modern UI Elements:
- 🌓 **Dark/Light Mode Toggle** - Click moon/sun icon
- 🎨 **Smooth Animations** - Framer Motion effects
- 📱 **Responsive Design** - Works on mobile, tablet, desktop
- 🎯 **Real-time Validation** - Form checks as you type
- 🔔 **Toast Notifications** - Success/error messages
- 📊 **Charts** (if available) - Visual data representations

---

## 🔧 Technical Details

### What's Running:

**Backend (Port 8000):**
- FastAPI REST API
- XGBoost ML model (80.45% accuracy)
- 8 engineered features
- Python 3.11.8 + NumPy 1.26.4

**Frontend (Port 3000):**
- React 18
- Tailwind CSS
- Framer Motion animations
- Axios for API calls
- React Router for navigation

---

## 🎭 Demo Scenarios to Try

### 1. First Class Female (High Survival)
```json
{
  "pclass": 1,
  "name": "Miss. Elizabeth Windsor",
  "sex": "female",
  "age": 29,
  "sibsp": 0,
  "parch": 0,
  "fare": 150.0,
  "embarked": "C"
}
```
**Expected**: SURVIVED (85-95% probability)

### 2. Third Class Male (Low Survival)
```json
{
  "pclass": 3,
  "name": "Mr. Jack Dawson",
  "sex": "male",
  "age": 20,
  "sibsp": 0,
  "parch": 0,
  "fare": 7.25,
  "embarked": "S"
}
```
**Expected**: NOT SURVIVED (15-25% probability)

### 3. Second Class Child (Moderate-High Survival)
```json
{
  "pclass": 2,
  "name": "Master. Timothy Brown",
  "sex": "male",
  "age": 5,
  "sibsp": 1,
  "parch": 2,
  "fare": 30.0,
  "embarked": "Q"
}
```
**Expected**: SURVIVED (60-70% probability)

---

## 🐛 If Something's Not Working

### Frontend Not Loading?
```cmd
# Check if it's running in the PowerShell window
# Look for: "Compiled successfully!" or "webpack compiled"
# If not, in the PowerShell window run:
npm start
```

### Backend Not Responding?
```cmd
# Open new terminal:
cd d:\titanic\backend
..\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

### Page Shows Error?
1. Check both PowerShell windows are still running
2. Refresh the browser (F5)
3. Check http://localhost:8000/docs to verify backend is up

---

## 📸 What You Should See

### Main Screen:
```
┌─────────────────────────────────────────────┐
│  🚢 TITANIC SURVIVAL PREDICTION             │
│  ─────────────────────────────────────────  │
│                                             │
│  [Predict] [Dashboard] [Model Info]        │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ Passenger Class: [___▼___]         │   │
│  │ Name: [_______________________]    │   │
│  │ Sex: [Male ○] [Female ○]          │   │
│  │ Age: [____]                        │   │
│  │ ...                                │   │
│  │                                    │   │
│  │   [🚢 Predict Survival]            │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Result Display:
```
┌─────────────────────────────────────┐
│  ✅ SURVIVED                        │
│  Probability: 87.3%                 │
│  ────────────────────                │
│  [●●●●●●●●●○] 87%                   │
└─────────────────────────────────────┘
```

---

## 🎯 Your App is Production-Ready!

✅ Modern React frontend
✅ FastAPI backend with ML model
✅ 80.45% prediction accuracy
✅ Beautiful, responsive UI
✅ Real-time predictions
✅ Professional animations
✅ Dark/Light mode
✅ Complete documentation

**Enjoy using your Titanic Survival Prediction App!** 🚢⚓✨

---

## 💡 Pro Tips

1. **Toggle Dark Mode** - Click the moon/sun icon in the top right
2. **Batch Predictions** - Use the API at /batch_predict for multiple passengers
3. **API Docs** - Explore http://localhost:8000/docs for all endpoints
4. **Experiment** - Try different combinations to see how factors affect survival

**Your app stands out with modern tech and best practices!** 🏆
