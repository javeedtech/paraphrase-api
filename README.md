# Paraphrasing API 🔄

A professional Flask-based REST API service that provides AI-powered text paraphrasing capabilities. Built for easy deployment and RapidAPI monetization.

## 🚀 Features

- **AI-Powered Paraphrasing**: Uses Hugging Face models with intelligent fallback patterns
- **Rate Limited**: 60 requests per minute per IP for fair usage
- **Production Ready**: Built with proper error handling, logging, and health checks
- **Easy Deployment**: Ready for Northflank, Railway, or any container platform
- **RapidAPI Compatible**: Designed for immediate monetization
- **Professional UI**: Beautiful dark-themed demo interface

## 🛠 Tech Stack

- **Backend**: Flask, Python 3.11
- **AI**: Hugging Face Inference API + intelligent fallback patterns
- **Frontend**: Bootstrap 5 with dark theme
- **Deployment**: Docker + Northflank
- **Rate Limiting**: Custom sliding window implementation

## 📚 API Documentation

### Base URL
```
https://your-domain.com/api
```

### Endpoints

#### POST `/api/paraphrase`
Paraphrase text using AI models.

**Request:**
```json
{
  "text": "The quick brown fox jumps over the lazy dog",
  "max_length": 100,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "success": true,
  "original_text": "The quick brown fox jumps over the lazy dog",
  "paraphrased_text": "A fast brown fox leaps over a sleepy dog",
  "processing_time_seconds": 0.234,
  "parameters": {
    "max_length": 100,
    "temperature": 0.7
  }
}
```

#### GET `/api/status`
Get API and model status.

#### GET `/health`
Health check endpoint.

## 🔧 Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/paraphrasing-api
   cd paraphrasing-api
   ```

2. **Install dependencies**
   ```bash
   pip install uv
   uv sync
   ```

3. **Run the application**
   ```bash
   uv run python main.py
   ```

4. **Visit the demo**: http://localhost:5000

## 🚢 Deployment

### Northflank (Recommended)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Northflank**:
   - Connect your GitHub repository
   - Use the included `northflank.json` configuration
   - Set optional `HF_TOKEN` environment variable for enhanced AI features

### Docker

```bash
docker build -t paraphrasing-api .
docker run -p 5000:5000 paraphrasing-api
```

## 💰 RapidAPI Integration

This API is designed for immediate RapidAPI monetization:

- ✅ RESTful JSON API
- ✅ Proper HTTP status codes
- ✅ Built-in rate limiting
- ✅ Comprehensive error handling
- ✅ Health check endpoints
- ✅ Professional documentation

### Suggested Pricing Tiers:
- **Basic**: $0.01 per request (1,000 requests/month)
- **Pro**: $0.005 per request (10,000 requests/month)
- **Enterprise**: $0.002 per request (100,000+ requests/month)

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SESSION_SECRET` | Yes | Flask session secret key |
| `HF_TOKEN` | No | Hugging Face API token for enhanced AI features |

## 📊 Monitoring

- Health endpoint: `/health`
- Status endpoint: `/api/status`
- Built-in logging for all requests
- Rate limiting with detailed error responses

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- [Live Demo](https://your-domain.com)
- [API Documentation](https://your-domain.com/docs)
- [RapidAPI Listing](https://rapidapi.com/your-api)