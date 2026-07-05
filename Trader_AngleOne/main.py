import io
import time
import pyotp
import logging
import contextlib
import pandas as pd
from .map_stock import stocklist
from SmartApi import SmartConnect
from datetime import datetime, timedelta



class TraderAngleOne:
    def __init__(self, api_key, secret_key, totp, userid, pwd,**kwargs):
        # Initialize API credentials
        self.api_key = api_key
        self.secret_key = secret_key
        self.totp = totp
        self.userid = userid
        self.pwd = pwd

        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.smartApi = SmartConnect(api_key=self.api_key)
        
        print('\n',20*'-',"YOU ARE LOGIN",20*'-','\n')
        self._generate_session()
        
        self.TIMEFRAME_MAPPING = {
            '1': "ONE_MINUTE",
            '3': "THREE_MINUTE",
            '5': "FIVE_MINUTE",
            '10': "TEN_MINUTE",
            '15': "FIFTEEN_MINUTE",
            '30': "THIRTY_MINUTE",
            "1H": "ONE_HOUR",
            "1D": "ONE_DAY",
        }
        
    def _generate_session(self):
        """Generate a session with the API."""
        data = self.smartApi.generateSession(self.userid, self.pwd, pyotp.TOTP(self.totp).now())
        self.autoken = data['data']['jwtToken']
        self.refreshToken = data['data']['refreshToken']
        self.smartApi.getProfile(self.refreshToken)
        self.feedtoken = self.smartApi.getfeedToken()
        
    def _fetch_historical_data(self, symbol, interval, fromdate, todate,exchange='NSE', max_retries=3, retry_delay=1):
        """Helper function to fetch historical data with retry logic."""
        token = stocklist.get(symbol)
        if not token:
            raise ValueError(f"Symbol {symbol} not found in stocklist.")

        for attempt in range(max_retries):
            try:
                historicParam = {
                    "exchange": exchange,
                    "symboltoken": token,
                    "interval": self.TIMEFRAME_MAPPING.get(interval),
                    "fromdate": fromdate,
                    "todate": todate
                }
                response = self.smartApi.getCandleData(historicParam)
                if not response or 'data' not in response or not response['data']:
                    raise ValueError("No data found in API response.")
                
                historicalData = pd.DataFrame(response['data'])
                if len(historicalData.columns) >= 6:
                    historicalData = historicalData.rename(columns={
                        0: "Datetime",  # Assuming the first column is the timestamp
                        1: "o",  # Open
                        2: "h",  # High
                        3: "l",  # Low
                        4: "c",  # Close
                        5: "vol"  # Volume
                    })
                else:
                    raise ValueError("API response does not contain enough columns.")
                
                historicalData["Datetime"] = pd.to_datetime(historicalData["Datetime"])
                historicalData = historicalData.set_index('Datetime')
                return historicalData
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {symbol}: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Max retries reached for {symbol}. Skipping this symbol.")
                    return None 
    
    # angle.get_history_data(stockName,'5',f'2023-01-02 09:15',f'2023-01-02 15:30')
    def get_history_data(self, symbol, interval, fromdate, todate,exchange="NSE"):
        """Get historical data for a specific period."""
        ff    = fromdate[:10]
        to      = todate[:10]
        ff    = datetime.strptime(ff, '%Y-%m-%d')
        to      = datetime.strptime(to, '%Y-%m-%d')

    
        if (ff > to) or (ff > datetime.strptime(datetime.now().strftime("%Y-%m-%d") + " 00:00:00", "%Y-%m-%d %H:%M:%S")):
            print(f"Provided date {fromdate} is a holiday. Try for the next date.")
            return None
        
        return self._fetch_historical_data(symbol, interval, fromdate, todate,exchange)
    
    


