# Deployment Guide 🚀

## FIXED: Northflank Deployment Issue

**Problem Resolved**: The original deployment error was caused by uv.lock dependency conflicts with PyTorch/Transformers packages. This has been fixed by updating the Dockerfile to use standard pip installation.

## Step-by-Step Deployment to Northflank

### 1. Push Your Code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial paraphrasing API implementation"

# Add your GitHub repository as origin
git remote add origin https://github.com/YOUR_USERNAME/paraphrasing-api

# Push to GitHub
git push -u origin main
```

### 2. Deploy on Northflank

1. **Sign up** at [northflank.com](https://northflank.com)
2. **Create a new service**
3. **Connect GitHub**: Link your GitHub account
4. **Select repository**: Choose your paraphrasing-api repository
5. **Configure deployment**:
   - **Name**: `paraphrasing-api`
   - **Branch**: `main`
   - **Build type**: `Dockerfile`
   - **Port**: `5000`

### 3. Environment Variables (Optional)

Set these in Northflank dashboard:

| Variable | Value | Required |
|----------|-------|----------|
| `SESSION_SECRET` | Random secure string | Yes |
| `HF_TOKEN` | Your Hugging Face API token | No |

**Getting Hugging Face Token** (for enhanced AI features):
1. Sign up at [huggingface.co](https://huggingface.co)
2. Go to Settings > Access Tokens
3. Create a new token
4. Add it as `HF_TOKEN` environment variable

### 4. Domain Configuration

After deployment:
1. **Custom Domain** (optional): Add your domain in Northflank settings
2. **SSL Certificate**: Automatically provided
3. **API URL**: Use the provided `.northflank.app` domain or your custom domain

### 5. Testing Your Deployment

```bash
# Test health endpoint
curl https://your-app.northflank.app/health

# Test paraphrasing
curl -X POST https://your-app.northflank.app/api/paraphrase \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "temperature": 0.7}'
```

## Alternative Deployment Options

### Railway

1. Connect GitHub repository
2. Deploy automatically
3. Cost: $5/month

### Render

1. Connect GitHub repository  
2. Use `gunicorn --bind 0.0.0.0:$PORT main:app`
3. Cost: $7/month

### DigitalOcean App Platform

1. Create new app from GitHub
2. Use provided Dockerfile
3. Cost: $5/month

## RapidAPI Integration

### 1. List Your API

1. **Sign up** at [rapidapi.com](https://rapidapi.com)
2. **Add API**: Use your deployed URL as base URL
3. **Configure endpoints**:
   - `POST /api/paraphrase`
   - `GET /api/status`
   - `GET /health`

### 2. Pricing Strategy

**Recommended tiers**:
- **Basic**: $0.01 per request (up to 1,000/month)
- **Pro**: $0.005 per request (up to 10,000/month)  
- **Enterprise**: $0.002 per request (100,000+/month)

### 3. API Description Template

```
# AI-Powered Paraphrasing API

Transform any text with advanced AI paraphrasing. Perfect for:
- Content creation and rewriting
- Academic writing assistance  
- SEO content optimization
- Plagiarism avoidance

## Features
✅ 99.9% uptime guarantee
✅ Fast response times (<1s)
✅ Rate limiting protection
✅ Professional error handling
✅ Comprehensive documentation
```

## Monitoring & Maintenance

### Health Monitoring

- **Health endpoint**: `/health`
- **Status monitoring**: `/api/status`
- **Uptime monitoring**: Use UptimeRobot or similar

### Logs

Check application logs in Northflank dashboard:
- Request/response logs
- Error tracking
- Performance metrics

### Scaling

Northflank auto-scales based on:
- CPU usage
- Memory usage  
- Request volume

## Costs Breakdown

### Free Tier (Getting Started)
- **Northflank**: Free tier (2 services)
- **Hugging Face**: Free tier (30K characters/month)
- **GitHub**: Free for public repos
- **RapidAPI**: Free to list (commission on sales)

**Total startup cost**: $0

### Production Scaling
- **Northflank**: $2.71/month minimum
- **Hugging Face Pro**: $9/month (1M characters)
- **Custom domain**: $10-15/year

**Monthly cost when profitable**: $12-25/month

## Revenue Potential

### Conservative Estimates
- **100 API calls/day** at $0.01 = $30/month revenue
- **500 API calls/day** at $0.005 = $75/month revenue
- **1000 API calls/day** at $0.002 = $60/month revenue

**Break-even**: ~40 API calls per day

### Growth Scenarios
- **RapidAPI marketplace exposure**
- **SEO content tools integration**
- **Academic writing platforms**
- **Content management systems**

## Success Tips

1. **Optimize listings**: Use good SEO keywords
2. **Monitor performance**: Keep response times low
3. **Gather feedback**: Improve based on user needs
4. **Marketing**: Share on developer communities
5. **Feature expansion**: Add batch processing, custom models

## Support

- **Documentation**: Available at `/docs`
- **GitHub Issues**: For technical problems
- **RapidAPI Support**: For marketplace issues