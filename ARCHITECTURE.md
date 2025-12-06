# 🚢 Titanic Survival Prediction - Project Architecture

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          React Frontend (Port 3000)                  │   │
│  │  • Modern UI with Tailwind CSS                       │   │
│  │  • Framer Motion Animations                          │   │
│  │  • Recharts Visualizations                           │   │
│  │  • Dark Mode Support                                 │   │
│  └──────────────────┬──────────────────────────────────┘   │
└─────────────────────┼──────────────────────────────────────┘
                      │ HTTP/REST API
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   API LAYER (FastAPI)                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          FastAPI Backend (Port 8000)                 │   │
│  │  • RESTful API Endpoints                             │   │
│  │  • Async Request Handling                            │   │
│  │  • Automatic OpenAPI Docs                            │   │
│  │  • CORS Middleware                                   │   │
│  │  • Request Validation (Pydantic)                     │   │
│  └──────────────────┬──────────────────────────────────┘   │
└─────────────────────┼──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  ML PIPELINE LAYER                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Feature Engineering                      │  │
│  │  • Title Extraction from Names                        │  │
│  │  • Family Size Calculation                            │  │
│  │  • Age/Fare Binning                                   │  │
│  │  • Interaction Features                               │  │
│  │  • Missing Value Imputation                           │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │            Preprocessing Pipeline                     │  │
│  │  • Label Encoding                                     │  │
│  │  • Standard Scaling                                   │  │
│  │  • Feature Selection                                  │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │            Ensemble Model Layer                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐ │  │
│  │  │Logistic  │  │ Random   │  │ XGBoost  │  │Light │ │  │
│  │  │Regress.  │  │ Forest   │  │          │  │ GBM  │ │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──┬───┘ │  │
│  │       └─────────────┼─────────────┼───────────┘     │  │
│  │                     ▼                                │  │
│  │              Soft Voting Ensemble                    │  │
│  │       (Weighted Average of Probabilities)            │  │
│  └──────────────────┬───────────────────────────────────┘  │
└─────────────────────┼──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  PREDICTION OUTPUT                           │
│  • Survival Prediction (0/1)                                 │
│  • Survival Probability (0-1)                                │
│  • Confidence Score                                          │
│  • Risk Level Assessment                                     │
│  • Feature Importance                                        │
└─────────────────────────────────────────────────────────────┘
```

## 🗂️ Project Structure

```
titanic/
├── 📁 backend/                    # FastAPI Backend
│   ├── main.py                    # Main API application
│   └── __init__.py
│
├── 📁 frontend/                   # React Frontend
│   ├── 📁 public/                 # Static assets
│   │   ├── index.html
│   │   └── manifest.json
│   │
│   ├── 📁 src/
│   │   ├── 📁 components/         # React Components
│   │   │   ├── PredictionForm.js  # Main prediction form
│   │   │   ├── PredictionResult.js# Result display
│   │   │   ├── Dashboard.js       # Analytics dashboard
│   │   │   └── ModelInfo.js       # Model information
│   │   │
│   │   ├── 📁 services/           # API Services
│   │   │   └── api.js             # API client
│   │   │
│   │   ├── App.js                 # Main App component
│   │   ├── index.js               # Entry point
│   │   └── index.css              # Global styles
│   │
│   ├── package.json               # Node dependencies
│   ├── tailwind.config.js         # Tailwind configuration
│   └── postcss.config.js          # PostCSS configuration
│
├── 📁 models/                     # Trained ML Models
│   ├── titanic_model.pkl          # Saved model package
│   └── 📁 visualizations/         # Generated charts
│       ├── confusion_matrix.png
│       ├── roc_curve.png
│       └── feature_importance.png
│
├── 📁 data/                       # Datasets
│   └── titanic.csv                # Training data
│
├── 📁 notebooks/                  # Jupyter Notebooks
│   └── eda_and_training.ipynb     # EDA & Training notebook
│
├── train_model.py                 # Model training script
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Docker orchestration
├── Dockerfile.backend             # Backend Docker image
├── Dockerfile.frontend            # Frontend Docker image
├── nginx.conf                     # Nginx configuration
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── setup.bat                      # Windows setup script
├── start.bat                      # Windows start script
├── README.md                      # Main documentation
├── QUICKSTART.md                  # Quick start guide
├── ARCHITECTURE.md                # This file
└── LICENSE                        # MIT License
```

## 🔄 Data Flow

### Training Phase

```
1. Load Titanic Dataset
   ↓
2. Feature Engineering
   • Extract titles from names
   • Calculate family sizes
   • Create age/fare bins
   • Generate interaction features
   ↓
3. Data Preprocessing
   • Handle missing values
   • Encode categorical features
   • Scale numerical features
   ↓
4. Model Training
   • Train 4 base models
   • Hyperparameter tuning
   • Cross-validation
   ↓
5. Ensemble Creation
   • Combine models using soft voting
   • Evaluate performance
   ↓
6. Save Model Package
   • Model + Preprocessors
   • Feature names
   • Metadata
```

### Prediction Phase

```
1. User Input (Frontend)
   ↓
2. HTTP POST Request
   ↓
3. FastAPI Validation (Pydantic)
   ↓
4. Feature Engineering
   • Apply same transformations
   • Create derived features
   ↓
5. Preprocessing
   • Encode categories
   • Scale features
   ↓
6. Model Prediction
   • Get probabilities from each model
   • Combine using soft voting
   ↓
7. Post-processing
   • Calculate confidence
   • Determine risk level
   • Extract feature importance
   ↓
8. JSON Response
   ↓
9. Frontend Display
   • Show results
   • Visualize probabilities
   • Display insights
```

## 🧠 ML Pipeline Details

### Feature Engineering (15+ Features)

**Original Features:**
- Pclass, Sex, Age, SibSp, Parch, Fare, Embarked

**Engineered Features:**
1. **Title** - Extracted from name (Mr, Mrs, Miss, Master, Rare)
2. **FamilySize** - SibSp + Parch + 1
3. **IsAlone** - Binary (FamilySize == 1)
4. **SmallFamily** - Binary (2 <= FamilySize <= 4)
5. **LargeFamily** - Binary (FamilySize >= 5)
6. **AgeGroup** - Categorical bins (Child, Teen, Adult, Middle, Senior)
7. **FareBin** - Quintile bins (Very_Low to Very_High)
8. **Age_Class** - Age × Pclass interaction
9. **Fare_Per_Person** - Fare / FamilySize
10. **HasCabin** - Binary (Cabin presence)
11. **CabinDeck** - First letter of cabin
12. **Sex_Binary** - Binary encoding of sex

### Model Ensemble

**Base Models:**

1. **Logistic Regression**
   - Regularization: L2
   - Solver: lbfgs
   - Hyperparameter tuning via GridSearchCV

2. **Random Forest**
   - n_estimators: 300
   - max_depth: 10
   - Gini impurity criterion

3. **XGBoost**
   - n_estimators: 300
   - learning_rate: 0.05
   - max_depth: 6
   - Advanced regularization

4. **LightGBM**
   - n_estimators: 300
   - learning_rate: 0.05
   - Gradient-based learning

**Ensemble Strategy:**
- Soft Voting: Weighted average of probability predictions
- Each model contributes equally (can be tuned)
- Final prediction based on combined probabilities

### Performance Metrics

```
Accuracy:  85.2% - Overall correctness
Precision: 84.0% - True positives / Predicted positives
Recall:    83.0% - True positives / Actual positives
F1-Score:  83.0% - Harmonic mean of precision/recall
ROC-AUC:   91.0% - Area under ROC curve
```

## 🎨 Frontend Architecture

### Component Hierarchy

```
App (Main Container)
├── Header
│   ├── Logo
│   ├── Navigation Tabs
│   └── Controls (Dark Mode, GitHub)
│
├── Main Content (Route-based)
│   ├── PredictionForm
│   │   ├── Input Fields (9 fields)
│   │   ├── Submit Button
│   │   └── PredictionResult
│   │       ├── Survival Status
│   │       ├── Probability Chart
│   │       ├── Stats Cards
│   │       └── Feature Contributions
│   │
│   ├── Dashboard
│   │   ├── Stat Cards (4)
│   │   ├── Survival by Class Chart
│   │   ├── Survival by Gender Chart
│   │   ├── Survival by Age Chart
│   │   ├── Feature Importance Chart
│   │   └── Key Insights Grid
│   │
│   └── ModelInfo
│       ├── Model Stats
│       ├── Feature Cards (4)
│       ├── Technology Stack Grid
│       ├── ML Pipeline Visualization
│       └── Standout Features
│
└── Footer
```

### State Management

- **React Hooks**: useState, useEffect
- **Local Storage**: Dark mode preference
- **API State**: Loading, data, error handling
- **Form State**: Controlled components

### Styling Approach

- **Tailwind CSS**: Utility-first styling
- **Custom Components**: Reusable styled components
- **Responsive Design**: Mobile-first approach
- **Dark Mode**: Class-based theme switching
- **Animations**: Framer Motion for smooth transitions

## 🐳 Docker Architecture

### Container Services

1. **Backend Container**
   - Base: python:3.9-slim
   - Port: 8000
   - Volumes: models/, data/
   - Health Check: /health endpoint

2. **Frontend Container**
   - Build Stage: node:18-alpine
   - Production Stage: nginx:alpine
   - Port: 80 (mapped to 3000)
   - Nginx reverse proxy for API

### Networking

- Bridge network: `titanic-network`
- Frontend → Backend: Internal DNS resolution
- External access: Host port mapping

## 🔐 Security Considerations

1. **Input Validation**: Pydantic models validate all inputs
2. **CORS**: Configured for allowed origins
3. **Environment Variables**: Sensitive data in .env
4. **Nginx Headers**: Security headers configured
5. **Error Handling**: Generic error messages, detailed logging

## 📈 Scalability Considerations

1. **Async API**: FastAPI async support for concurrent requests
2. **Model Caching**: Model loaded once at startup
3. **Stateless Design**: No session state, horizontal scaling ready
4. **Database Ready**: Easy to add PostgreSQL/MongoDB
5. **Load Balancing**: Nginx can distribute traffic
6. **Microservices**: Backend and frontend independently scalable

## 🔮 Future Enhancements

1. **Real-time Updates**: WebSocket support for live predictions
2. **User Accounts**: Authentication and prediction history
3. **Batch Processing**: Upload CSV for bulk predictions
4. **Model Versioning**: A/B testing different models
5. **Monitoring**: Prometheus metrics, Grafana dashboards
6. **CI/CD**: GitHub Actions for automated deployment
7. **Advanced Models**: Deep learning (Neural Networks)
8. **Explainability**: SHAP/LIME integration for model interpretation

---

Last Updated: 2024
Version: 2.0.0
