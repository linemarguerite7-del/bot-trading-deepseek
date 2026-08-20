# bot-trading-deepseek

Bot de trading pour mission Sophia

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Running

```bash
python bot_trading.py
```

## Deployment

This project is configured for deployment on [Render](https://render.com).

The `render.yaml` file at the repository root defines the deployment configuration:
- **Runtime**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python bot_trading.py`
- **Region**: Oregon
- **Plan**: Free

To deploy:
1. Connect this repository to your Render account
2. Render will automatically detect and use `render.yaml`
3. The service will build and start automatically

## Environment Variables

- `PYTHONUNBUFFERED=1` - Ensures Python output is sent straight to logs

## Project Structure

- `bot_trading.py` - Main bot entry point
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment configuration
