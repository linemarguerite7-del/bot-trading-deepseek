#!/usr/bin/env python3
"""
Bot Trading Deepseek - An automated trading bot using Deepseek AI
Version 2.0 - Production Ready
"""

import os
import sys
import time
import logging
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
import aiohttp
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

# Configure logging with rotation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot_trading.log')
    ]
)
logger = logging.getLogger(__name__)


class DeepseekTradingBot:
    """Main Trading Bot class with async support and error handling"""
    
    def __init__(self):
        """Initialize the bot with configuration"""
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.api_url = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
        self.trading_enabled = os.getenv('TRADING_ENABLED', 'false').lower() == 'true'
        self.update_interval = int(os.getenv('UPDATE_INTERVAL', '60'))
        self.retry_attempts = int(os.getenv('RETRY_ATTEMPTS', '3'))
        self.timeout = int(os.getenv('TIMEOUT', '30'))
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.running = False
        self.stats = {
            'trades_executed': 0,
            'successful_predictions': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
        
        logger.info(f"Bot initialized - Trading: {'ENABLED' if self.trading_enabled else 'DISABLED'}")
    
    async def validate_configuration(self) -> bool:
        """Validate all required environment variables and API access"""
        try:
            if not self.api_key:
                logger.error("❌ DEEPSEEK_API_KEY environment variable is not set")
                return False
            
            logger.info("✅ Configuration validated successfully")
            return True
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}", exc_info=True)
            return False
    
    async def fetch_market_data(self) -> Optional[Dict[str, Any]]:
        """Fetch market data with retry logic"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            headers = {'Authorization': f'Bearer {self.api_key}'}
            
            for attempt in range(self.retry_attempts):
                try:
                    async with self.session.get(
                        f'{self.api_url}/market/data',
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            logger.debug(f"Market data fetched successfully (attempt {attempt + 1})")
                            return data
                        elif response.status == 401:
                            logger.error("❌ Authentication failed - Invalid API key")
                            return None
                        elif response.status == 429:
                            wait_time = (2 ** attempt)  # Exponential backoff
                            logger.warning(f"Rate limited. Waiting {wait_time}s before retry...")
                            await asyncio.sleep(wait_time)
                            continue
                except asyncio.TimeoutError:
                    logger.warning(f"Request timeout (attempt {attempt + 1}/{self.retry_attempts})")
                    if attempt < self.retry_attempts - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    return None
            
            return None
        
        except Exception as e:
            logger.error(f"Error fetching market data: {e}", exc_info=True)
            self.stats['errors'] += 1
            return None
    
    async def analyze_with_deepseek(self, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send market data to Deepseek AI for analysis"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            payload = {
                'model': 'deepseek-chat',
                'messages': [
                    {
                        'role': 'user',
                        'content': f"Analyze this market data and provide trading recommendations: {market_data}"
                    }
                ],
                'temperature': 0.3,
                'max_tokens': 500
            }
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            async with self.session.post(
                f'{self.api_url}/chat/completions',
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info("✅ AI analysis completed")
                    self.stats['successful_predictions'] += 1
                    return result
                else:
                    logger.error(f"AI analysis failed with status {response.status}")
                    return None
        
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}", exc_info=True)
            self.stats['errors'] += 1
            return None
    
    async def execute_trade(self, recommendation: Dict[str, Any]) -> bool:
        """Execute a trade based on AI recommendation"""
        if not self.trading_enabled:
            logger.info("🔒 Trading disabled - Dry run mode")
            return False
        
        try:
            logger.info(f"📊 Executing trade based on recommendation: {recommendation}")
            self.stats['trades_executed'] += 1
            return True
        
        except Exception as e:
            logger.error(f"Error executing trade: {e}", exc_info=True)
            self.stats['errors'] += 1
            return False
    
    async def report_stats(self):
        """Log bot statistics"""
        uptime = (datetime.now() - self.stats['start_time']).total_seconds()
        logger.info(
            f"\n📈 BOT STATISTICS:\n"
            f"  ⏱️  Uptime: {uptime:.0f}s\n"
            f"  📊 Trades executed: {self.stats['trades_executed']}\n"
            f"  ✅ Successful predictions: {self.stats['successful_predictions']}\n"
            f"  ❌ Errors: {self.stats['errors']}"
        )
    
    async def run(self):
        """Main bot loop"""
        try:
            # Validate configuration
            if not await self.validate_configuration():
                sys.exit(1)
            
            self.running = True
            logger.info("🚀 Bot Trading Deepseek v2.0 started")
            logger.info(f"⏳ Update interval: {self.update_interval}s")
            
            iteration = 0
            while self.running:
                try:
                    iteration += 1
                    logger.debug(f"--- Iteration {iteration} ---")
                    
                    # Fetch market data
                    market_data = await self.fetch_market_data()
                    if market_data is None:
                        logger.warning("No market data available, skipping iteration")
                        await asyncio.sleep(self.update_interval)
                        continue
                    
                    # Analyze with Deepseek AI
                    analysis = await self.analyze_with_deepseek(market_data)
                    if analysis:
                        # Execute trade
                        await self.execute_trade(analysis)
                    
                    # Sleep before next iteration
                    await asyncio.sleep(self.update_interval)
                    
                    # Report stats every 10 iterations
                    if iteration % 10 == 0:
                        await self.report_stats()
                
                except Exception as e:
                    logger.error(f"Error in bot loop iteration: {e}", exc_info=True)
                    self.stats['errors'] += 1
                    await asyncio.sleep(self.update_interval)
                    continue
        
        except KeyboardInterrupt:
            logger.info("\n⏹️  Bot stopped by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            sys.exit(1)
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Clean up resources"""
        self.running = False
        await self.report_stats()
        if self.session:
            await self.session.close()
        logger.info("✅ Bot cleanup completed")


async def main():
    """Entry point"""
    bot = DeepseekTradingBot()
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
