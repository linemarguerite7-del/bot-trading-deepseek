# 🤖 Bot Trading Deepseek v2.0

**An advanced, production-ready automated trading bot powered by Deepseek AI**

## ✨ Features

- 🤖 **AI-Powered Analysis** - Uses Deepseek Chat API for intelligent market analysis
- ⚡ **Async Architecture** - High-performance async/await for concurrent operations
- 🔄 **Robust Error Handling** - Automatic retry logic with exponential backoff
- 📊 **Real-time Monitoring** - Comprehensive logging and statistics tracking
- 🔒 **Dry-Run Mode** - Test strategies without executing actual trades
- 🛡️ **Production Ready** - Error recovery, timeouts, and graceful shutdown
- 📝 **Full Configuration** - Environment-based configuration system

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- Deepseek API key ([Get one here](https://deepseek.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/linemarguerite7-del/bot-trading-deepseek.git
cd bot-trading-deepseek

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your DEEPSEEK_API_KEY
```

### Running the Bot

```bash
# Run in dry-run mode (no actual trades)
python bot_trading.py

# Run with trading enabled (set TRADING_ENABLED=true in .env)
TRADING_ENABLED=true python bot_trading.py
```

## 📋 Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Required
DEEPSEEK_API_KEY=your_api_key_here

# Optional (defaults shown)
DEEPSEEK_API_URL=https://api.deepseek.com/v1
TRADING_ENABLED=false           # Set to 'true' to enable actual trades
UPDATE_INTERVAL=60              # Seconds between market checks
RETRY_ATTEMPTS=3                # Number of retry attempts
TIMEOUT=30                      # Request timeout in seconds
LOG_LEVEL=INFO
```

## 📊 Project Structure

```
.
├── bot_trading.py           Main bot application
├── config.py                Configuration management
├── requirements.txt         Python dependencies
├── .env.example             Environment template
├── render.yaml              Render deployment config
├── bot_trading.log          Application logs (generated)
└── README.md                This file
```

## 🔄 How It Works

1. **Market Data Fetching** - Retrieves current market data with error handling
2. **AI Analysis** - Sends data to Deepseek AI for intelligent analysis
3. **Trade Execution** - Executes trades based on AI recommendations
4. **Monitoring** - Tracks statistics and logs all activity
5. **Retry Logic** - Automatically retries failed requests with exponential backoff

## 📈 Monitoring & Logs

The bot logs to both console and `bot_trading.log`:

```bash
# View live logs
tail -f bot_trading.log

# Search for errors
grep ERROR bot_trading.log

# View statistics
grep "BOT STATISTICS" bot_trading.log
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Test in dry-run mode
TRADING_ENABLED=false pytest tests/
```

## 🚢 Deployment

### On Render.com

1. Connect your GitHub repository to Render
2. Render automatically detects `render.yaml`
3. Set environment variables in Render dashboard:
   - `DEEPSEEK_API_KEY` - Your API key
   - `TRADING_ENABLED` - Set to `false` for safety
4. Deploy automatically on push

### Docker Deployment

```bash
# Build image
docker build -t bot-trading-deepseek .

# Run container
docker run -e DEEPSEEK_API_KEY=your_key bot-trading-deepseek
```

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEEPSEEK_API_KEY` | Required | Your Deepseek API key |
| `DEEPSEEK_API_URL` | https://api.deepseek.com/v1 | API endpoint |
| `TRADING_ENABLED` | false | Enable/disable actual trades |
| `UPDATE_INTERVAL` | 60 | Seconds between updates |
| `RETRY_ATTEMPTS` | 3 | Number of retry attempts |
| `TIMEOUT` | 30 | Request timeout (seconds) |
| `LOG_LEVEL` | INFO | Logging level |
| `PYTHONUNBUFFERED` | 1 | Unbuffered output |

## 🐛 Troubleshooting

### Bot doesn't start

```bash
# Check configuration
python -c "from config import get_config; c=get_config(); print(c.validate())"

# Verify API key
echo $DEEPSEEK_API_KEY
```

### High error rate

```bash
# Check logs for rate limiting
grep "Rate limited" bot_trading.log

# Increase timeout
echo "TIMEOUT=60" >> .env

# Decrease update frequency
echo "UPDATE_INTERVAL=120" >> .env
```

### Memory issues

```bash
# Monitor resource usage
ps aux | grep bot_trading.py

# Check for memory leaks in logs
grep "memory\|leak" bot_trading.log
```

## 📚 API Documentation

See [Deepseek API Docs](https://deepseek.com/docs) for:
- Chat completion endpoints
- Model selection
- Rate limits
- Authentication

## 🔐 Security

- ✅ Never commit `.env` files
- ✅ Store API keys in environment variables
- ✅ Use HTTPS for all API calls
- ✅ Validate all external input
- ✅ Run in dry-run mode by default

## 📝 Development

```bash
# Format code
black bot_trading.py config.py

# Lint code
flake8 bot_trading.py

# Type checking
mypy bot_trading.py
```

## 📄 License

Apache License 2.0 - See LICENSE file

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly
4. Submit a pull request

## 📞 Support

- 🐛 [Report Issues](https://github.com/linemarguerite7-del/bot-trading-deepseek/issues)
- 💬 [Discussions](https://github.com/linemarguerite7-del/bot-trading-deepseek/discussions)
- 📧 Contact: [GitHub Profile](https://github.com/linemarguerite7-del)

---

**⚠️ Disclaimer**: This bot is for educational purposes. Trading involves risk. Always test in dry-run mode first.
