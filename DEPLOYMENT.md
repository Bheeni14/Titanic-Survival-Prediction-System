# 🚀 Deployment Guide - Titanic Survival Predictor

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Checklist](#production-checklist)
- [Monitoring & Maintenance](#monitoring--maintenance)

---

## 📦 Local Development

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### Setup

```bash
# Clone repository
git clone <your-repo-url>
cd titanic

# Windows: Run setup script
setup.bat

# Linux/Mac: Manual setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train_model.py
```

### Running Locally

```bash
# Windows
start.bat

# Linux/Mac - Terminal 1 (Backend)
source venv/bin/activate
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Linux/Mac - Terminal 2 (Frontend)
cd frontend
npm install
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Containers

```bash
# Build images
docker build -f Dockerfile.backend -t titanic-backend .
docker build -f Dockerfile.frontend -t titanic-frontend .

# Run containers
docker run -d -p 8000:8000 --name backend titanic-backend
docker run -d -p 3000:80 --name frontend titanic-frontend

# Check status
docker ps
```

---

## ☁️ Cloud Deployment

### Option 1: AWS (Elastic Beanstalk)

#### Backend Deployment

```bash
# Install EB CLI
pip install awsebcli

# Initialize EB application
eb init -p python-3.9 titanic-backend --region us-east-1

# Create environment
eb create titanic-backend-prod

# Deploy
eb deploy

# Open app
eb open
```

**Configuration (`Dockerrun.aws.json`):**
```json
{
  "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "your-dockerhub/titanic-backend:latest",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": 8000
    }
  ]
}
```

#### Frontend Deployment (S3 + CloudFront)

```bash
# Build frontend
cd frontend
npm run build

# Install AWS CLI
pip install awscli

# Create S3 bucket
aws s3 mb s3://titanic-ml-app

# Configure as static website
aws s3 website s3://titanic-ml-app --index-document index.html

# Upload build
aws s3 sync build/ s3://titanic-ml-app --acl public-read

# Create CloudFront distribution
aws cloudfront create-distribution --origin-domain-name titanic-ml-app.s3.amazonaws.com
```

### Option 2: Google Cloud Platform (Cloud Run)

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Deploy backend
gcloud run deploy titanic-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000

# Deploy frontend
cd frontend
npm run build
gcloud app deploy
```

### Option 3: Microsoft Azure (App Service)

```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create resource group
az group create --name titanic-rg --location eastus

# Create App Service plan
az appservice plan create --name titanic-plan --resource-group titanic-rg --is-linux --sku B1

# Deploy backend
az webapp create --resource-group titanic-rg --plan titanic-plan --name titanic-backend-api --deployment-container-image-name your-dockerhub/titanic-backend:latest

# Deploy frontend
cd frontend
npm run build
az webapp up --resource-group titanic-rg --name titanic-frontend-app --html --src ./build
```

### Option 4: Heroku

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create apps
heroku create titanic-backend-api
heroku create titanic-frontend-app

# Deploy backend
git subtree push --prefix backend heroku main

# Deploy frontend
cd frontend
npm run build
# Use heroku-buildpack-static or deploy to S3
```

### Option 5: DigitalOcean (Droplet)

```bash
# Create Droplet (Ubuntu 22.04)
# Install Docker
ssh root@your-droplet-ip
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt-get update
apt-get install docker-compose-plugin

# Clone repository
git clone <your-repo-url>
cd titanic

# Create .env file
cp .env.example .env
# Edit .env with production values

# Start services
docker-compose up -d

# Setup Nginx reverse proxy
apt-get install nginx
# Configure nginx (see nginx configuration below)

# Setup SSL with Let's Encrypt
apt-get install certbot python3-certbot-nginx
certbot --nginx -d yourdomain.com
```

**Nginx Configuration (`/etc/nginx/sites-available/titanic`):**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Docs
    location /docs {
        proxy_pass http://localhost:8000/docs;
    }
}
```

### Option 6: Kubernetes (K8s)

**Backend Deployment (`k8s/backend-deployment.yaml`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: titanic-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: titanic-backend
  template:
    metadata:
      labels:
        app: titanic-backend
    spec:
      containers:
      - name: backend
        image: your-dockerhub/titanic-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: MODEL_PATH
          value: /app/models/titanic_model.pkl
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: titanic-backend-service
spec:
  selector:
    app: titanic-backend
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: LoadBalancer
```

```bash
# Apply configurations
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml

# Check status
kubectl get pods
kubectl get services

# Scale
kubectl scale deployment titanic-backend --replicas=5
```

---

## ✅ Production Checklist

### Security
- [ ] Update CORS allowed origins (no wildcard `*`)
- [ ] Set strong environment variables
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Implement rate limiting
- [ ] Add authentication if needed
- [ ] Regular security updates

### Performance
- [ ] Enable caching (Redis/Memcached)
- [ ] Setup CDN for frontend assets
- [ ] Optimize Docker images (multi-stage builds)
- [ ] Database connection pooling
- [ ] Enable Gzip compression
- [ ] Implement load balancing

### Monitoring
- [ ] Setup logging (ELK/Splunk)
- [ ] Configure monitoring (Prometheus/Grafana)
- [ ] Setup alerting (PagerDuty/Slack)
- [ ] Track API metrics
- [ ] Monitor model performance
- [ ] Setup error tracking (Sentry)

### Reliability
- [ ] Setup automated backups
- [ ] Configure health checks
- [ ] Implement graceful shutdown
- [ ] Setup auto-scaling
- [ ] Configure rolling updates
- [ ] Test disaster recovery

### Documentation
- [ ] API documentation current
- [ ] Deployment runbooks
- [ ] Incident response plan
- [ ] Architecture diagrams
- [ ] Environment configurations
- [ ] Troubleshooting guides

---

## 📊 Monitoring & Maintenance

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Check logs
docker-compose logs -f backend

# Monitor resources
docker stats
```

### Log Management

```python
# Add to backend/main.py
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler('logs/app.log', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
```

### Performance Monitoring

```python
# Add to backend/main.py
from prometheus_client import Counter, Histogram, generate_latest
import time

# Metrics
prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_duration = Histogram('prediction_duration_seconds', 'Prediction duration')

@app.post("/api/v1/predict")
async def predict_survival(passenger: PassengerInput):
    start_time = time.time()
    
    # ... prediction logic ...
    
    prediction_counter.inc()
    prediction_duration.observe(time.time() - start_time)
    
    return result

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Automated Backups

```bash
# Backup script (backup.sh)
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/titanic"

# Backup models
tar -czf $BACKUP_DIR/models_$DATE.tar.gz models/

# Backup data
tar -czf $BACKUP_DIR/data_$DATE.tar.gz data/

# Remove old backups (keep last 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

### Model Updates

```bash
# Retrain model with new data
python train_model.py --new-data data/updated_titanic.csv

# Test new model
python test_model.py

# Deploy new model (zero-downtime)
# 1. Save new model with version
# 2. Update MODEL_PATH environment variable
# 3. Restart backend gracefully
docker-compose restart backend
```

---

## 🆘 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Retrain model
python train_model.py
```

**Frontend build fails:**
```bash
# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

**Docker issues:**
```bash
# Clean Docker
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

---

## 📞 Support

For deployment issues:
1. Check logs: `docker-compose logs`
2. Review documentation
3. Open GitHub issue
4. Contact: your-email@example.com

---

**Last Updated:** 2024
**Version:** 2.0.0
