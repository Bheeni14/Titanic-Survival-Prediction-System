# 🚀 Installation Commands Reference

Quick copy-paste commands for setting up the Titanic Survival Predictor on different platforms.

---

## 🪟 Windows

### Quick Start (Automated)
```batch
# Clone repository
git clone <your-repo-url>
cd titanic

# Run automated setup
setup.bat

# Start application
start.bat
```

### Manual Setup
```batch
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Train model
python train_model.py

# Start backend (Terminal 1)
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (Terminal 2 - new window)
cd frontend
npm install
npm start
```

### Verify Installation
```batch
# Run verification script
verify.bat

# Test API
python test_api.py
```

---

## 🐧 Linux / macOS

### Quick Start
```bash
# Clone repository
git clone <your-repo-url>
cd titanic

# Make scripts executable
chmod +x setup.sh start.sh

# Run setup
./setup.sh

# Start application
./start.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Train model
python train_model.py

# Start backend (Terminal 1)
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (Terminal 2)
cd frontend
npm install
npm start
```

### Verify Installation
```bash
# Test API
python test_api.py

# Check if services are running
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## 🐳 Docker

### Using Docker Compose (Recommended)
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild without cache
docker-compose build --no-cache
docker-compose up
```

### Using Docker Manually
```bash
# Build images
docker build -f Dockerfile.backend -t titanic-backend:latest .
docker build -f Dockerfile.frontend -t titanic-frontend:latest .

# Create network
docker network create titanic-network

# Run backend
docker run -d \
  --name titanic-backend \
  --network titanic-network \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  titanic-backend:latest

# Run frontend
docker run -d \
  --name titanic-frontend \
  --network titanic-network \
  -p 3000:80 \
  titanic-frontend:latest

# Check status
docker ps

# View logs
docker logs titanic-backend
docker logs titanic-frontend
```

---

## ☁️ Cloud Platforms

### AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 titanic-app --region us-east-1

# Create environment
eb create titanic-prod

# Deploy
eb deploy

# Open application
eb open

# View logs
eb logs

# Terminate
eb terminate titanic-prod
```

### Google Cloud Platform
```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Deploy backend to Cloud Run
gcloud run deploy titanic-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Deploy frontend to App Engine
cd frontend
npm run build
gcloud app deploy
```

### Microsoft Azure
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Create resource group
az group create --name titanic-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name titanic-plan \
  --resource-group titanic-rg \
  --is-linux \
  --sku B1

# Deploy backend
az webapp create \
  --resource-group titanic-rg \
  --plan titanic-plan \
  --name titanic-backend \
  --deployment-container-image-name your-dockerhub/titanic-backend:latest

# Deploy frontend
cd frontend
npm run build
az webapp up \
  --resource-group titanic-rg \
  --name titanic-frontend \
  --html \
  --src ./build
```

### Heroku
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create apps
heroku create titanic-backend-api
heroku create titanic-frontend-app

# Deploy backend
cd backend
git init
heroku git:remote -a titanic-backend-api
git add .
git commit -m "Initial commit"
git push heroku main

# Deploy frontend
cd ../frontend
npm run build
# Use static buildpack
heroku buildpacks:set https://github.com/heroku/heroku-buildpack-static
echo '{"root": "build/"}' > static.json
git add .
git commit -m "Deploy frontend"
git push heroku main
```

### DigitalOcean
```bash
# Install doctl
cd ~
wget https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-linux-amd64.tar.gz
tar xf doctl-1.94.0-linux-amd64.tar.gz
sudo mv doctl /usr/local/bin

# Authenticate
doctl auth init

# Create Droplet
doctl compute droplet create titanic-app \
  --size s-2vcpu-4gb \
  --image ubuntu-22-04-x64 \
  --region nyc1 \
  --ssh-keys YOUR_SSH_KEY_ID

# SSH into Droplet
doctl compute ssh titanic-app

# On Droplet - Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Clone and run
git clone <your-repo-url>
cd titanic
docker compose up -d
```

---

## 🔧 Development Tools Installation

### Python
```bash
# Windows (using Chocolatey)
choco install python

# macOS (using Homebrew)
brew install python@3.9

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip

# Verify
python --version
```

### Node.js
```bash
# Windows (using Chocolatey)
choco install nodejs

# macOS (using Homebrew)
brew install node@18

# Linux (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version
npm --version
```

### Docker
```bash
# Windows
# Download Docker Desktop from: https://www.docker.com/products/docker-desktop

# macOS (using Homebrew)
brew install --cask docker

# Linux (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# Verify
docker --version
docker-compose --version
```

### Git
```bash
# Windows (using Chocolatey)
choco install git

# macOS (using Homebrew)
brew install git

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install git

# Verify
git --version
```

---

## 🧪 Testing Commands

### Backend Tests
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run API tests
python test_api.py

# Run unit tests (if pytest is installed)
pytest tests/ -v

# Check code style
flake8 backend/

# Type checking
mypy backend/
```

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Lint code
npm run lint

# Build production
npm run build
```

### Integration Tests
```bash
# Start services
docker-compose up -d

# Wait for services to be ready
sleep 10

# Test API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"pclass":1,"sex":"female","age":25,"sibsp":1,"parch":0,"fare":100,"embarked":"S"}'

# Test frontend
curl http://localhost:3000

# Stop services
docker-compose down
```

---

## 🔄 Update Commands

### Update Dependencies
```bash
# Python packages
pip install --upgrade -r requirements.txt

# Node packages
cd frontend
npm update

# Docker images
docker-compose pull
docker-compose up --build
```

### Update Code
```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt
cd frontend && npm install

# Retrain model if needed
python train_model.py

# Restart services
docker-compose restart
```

---

## 🗑️ Cleanup Commands

### Remove Virtual Environment
```bash
# Windows
rmdir /s venv

# Linux/Mac
rm -rf venv
```

### Remove Node Modules
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Clean Docker
```bash
# Stop all containers
docker-compose down

# Remove containers
docker rm titanic-backend titanic-frontend

# Remove images
docker rmi titanic-backend:latest titanic-frontend:latest

# Clean system (careful!)
docker system prune -a
```

### Full Reset
```bash
# Remove everything and start fresh
rm -rf venv node_modules models/*.pkl
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train_model.py
cd frontend && npm install
```

---

## 📊 Monitoring Commands

### Check Services
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check if frontend is running
curl http://localhost:3000

# Check Docker containers
docker ps

# Check logs
docker-compose logs -f

# Check resource usage
docker stats
```

### Performance Testing
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test API performance
ab -n 1000 -c 10 -p payload.json -T application/json \
  http://localhost:8000/api/v1/predict

# Where payload.json contains:
# {"pclass":1,"sex":"female","age":25,"sibsp":1,"parch":0,"fare":100,"embarked":"S"}
```

---

## 🆘 Troubleshooting Commands

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### Permission Errors
```bash
# Linux/Mac
sudo chown -R $USER:$USER .
chmod -R 755 .
```

### Module Not Found
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
cd frontend && npm install --force
```

---

## 📚 Help Commands

```bash
# Python help
python --help
pip --help

# Node help
node --help
npm --help

# Docker help
docker --help
docker-compose --help

# Git help
git --help

# API documentation
# Open: http://localhost:8000/docs
```

---

**Quick Access URLs:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

---

**Note**: Replace `<your-repo-url>` with your actual GitHub repository URL throughout these commands.
