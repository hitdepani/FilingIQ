# FilingIQ AWS Deployment Guide

## Architecture
- **EC2**: Ubuntu instance (t2.micro - FREE TIER)
- **ECR**: Docker image repository
- **GitHub Actions**: CI/CD pipeline
- **Route53**: DNS (optional)

## Prerequisites
1. AWS Account (free tier)
2. GitHub account with repo

## Step 1: Create EC2 Instance

1. Go to AWS Console → EC2
2. Click "Launch Instances"
3. Select "Ubuntu Server 24.04 LTS" (Free tier eligible)
4. Instance type: **t2.micro** (FREE)
5. Create new key pair: `filingiq-key.pem`
   - Save this file safely!
6. Security group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
7. Storage: 30GB (FREE tier allows up to 30GB)
8. Launch!

## Step 2: Connect to EC2

```bash
# Change permissions on key
chmod 400 filingiq-key.pem

# SSH into instance
ssh -i filingiq-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

## Step 3: Install Docker on EC2

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER

# Restart Docker
sudo systemctl restart docker
```

## Step 4: Clone repo and setup

```bash
# Clone your GitHub repo
git clone https://github.com/YOUR_USERNAME/filingiq.git
cd filingiq

# Create .env file
nano .env
# Paste: GROQ_API_KEY=your_key_here
# Save: Ctrl+X → Y → Enter

# Build and run
docker-compose up -d
```

## Step 5: Setup GitHub Secrets (for CI/CD)

1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `AWS_ACCESS_KEY_ID` (from AWS IAM)
   - `AWS_SECRET_ACCESS_KEY` (from AWS IAM)
   - `EC2_HOST` (your EC2 public IP)
   - `EC2_KEY` (content of filingiq-key.pem)
   - `GROQ_API_KEY` (your API key)

## Step 6: Auto-Deploy

Just push to main branch:
```bash
git push origin main
```

GitHub Actions will automatically:
1. Build Docker image
2. Push to AWS ECR
3. Deploy to EC2

## Monitoring

Check logs:
```bash
# SSH into EC2
ssh -i filingiq-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# View logs
docker logs filingiq-api -f

# Check running containers
docker ps
```

## Cost Estimate
- **EC2 t2.micro**: FREE (12 months)
- **Data transfer**: ~5GB free/month
- **ECR**: FREE (500MB storage)
- **Total**: $0 for 1 year