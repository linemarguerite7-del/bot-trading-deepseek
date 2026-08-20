# bot-trading-deepseek
Bot de trading pour mission Sophia 
services:
  - type: web
    name: bot-trading-deepseek
    env: python
    plan: free
    region: oregon
    repo: https://github.com/linemarguerite7-del/bot-trading-deepseek
    buildCommand: pip install -r requirements.txt
    startCommand: python bot_trading.py
    envVars:
      - key: PYTHONUNBUFFERED
        value: "1"
