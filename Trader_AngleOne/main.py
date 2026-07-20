import io
import time
import json
from SmartApi import smartWebSocketV2
from numpy import correlate
import pyotp
import logging
import contextlib
import pandas as pd
from typing import Any, Dict, cast
from .map_stock import stocklist
# from map_stock import stocklist
from SmartApi import SmartConnect 
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from datetime import datetime, timedelta



class TraderAngleOne:
    def __init__(self, api_key, secret_key, totp, userid, pwd,**kwargs):
        # Initialize API credentials
        self.api_key = api_key
        self.secret_key = secret_key
        self.totp = totp
        self.userid = userid
        self.pwd = pwd
        
        self.webSocket_Storage = {}

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
        response = self.smartApi.generateSession(self.userid, self.pwd, pyotp.TOTP(self.totp).now())
        response_data = cast(Dict[str, Any], response)
        session_data = cast(Dict[str, Any], response_data.get("data", {}))
        self.autoken = cast(str, session_data.get("jwtToken", ""))
        self.refreshToken = cast(str, session_data.get("refreshToken", ""))
        self.smartApi.getProfile(self.refreshToken)
        self.feedtoken = self.smartApi.getfeedToken()
        
        return {'authtoken':self.autoken,'feedtoken':self.feedtoken}
        
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
                if not response or not isinstance(response, dict) or 'data' not in response or not response['data']:
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
    
    def getLtp(self,exchange='NSE',symbol='SBIN',symbolToken= '3045'):
        symbolEQ = symbol.strip() + '-EQ'
        data = self.smartApi.ltpData(exchange=exchange,tradingsymbol=symbolEQ,symboltoken=symbolToken)
        return pd.DataFrame(data)
    
    def _process_price_update(self,token,ltp,websocketUpdate):
        self.webSocket_Storage[token] = ltp / 100
        try:
            print(f'updates - {ltp / 100}')
            with open(websocketUpdate, "w") as json_file:
                json.dump(self.webSocket_Storage, json_file, indent=4)
        except Exception as e:
            print(f"File Write Error - {e}")
            
        
    
    def AnglewebSocket(self,tmode=1,ListofToken=['3045'],websocketUpdate='./websocket_updatePrice.json'):
        
        correlation_id = 'stream_test'
        action = 1
        mode = tmode
        
        token_list = [
            {
                'exchangeType': 1,
                'tokens'  : ListofToken
             }
        ]
        auth = self._generate_session()
        self.sws = SmartWebSocketV2(auth['authtoken'], self.api_key,self.userid,auth['feedtoken'])
        
        def on_data(wsapp,data):
            token = data.get('token')
            ltp = data.get('last_traded_price')
            self._process_price_update(token, ltp,websocketUpdate)
            
        def on_open(wsapp):
            print('Websocket connect Sucessfully !!')
            self.sws.subscribe(correlation_id,mode,token_list)
        
        def on_error(error=None):
            print(f'Error: {error}')
        
        def on_close(wsapp):
            print('Websocket Close')

        self.sws.on_open = on_open
        self.sws.on_data = on_data
        self.sws.on_error = on_error
        self.sws.on_close = on_close
        
        self.sws.connect()
    
    def webSocket_Unsubscribe(self,mode=1,token_list=['3045']):
        self.sws.unsubscribe('unsubscribe_id',mode,token_list)
        for token in token_list:
            self.webSocket_Storage[token] = None