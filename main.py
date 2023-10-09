from fastapi import FastAPI, Query, HTTPException
import ccxt.async_support as ccxt
import os
from dotenv import load_dotenv
#from pymongo.mongo_client import MongoClient
import telegram
from typing import Annotated
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

USDT = 'USDT'
load_dotenv()
MIN_BALANCE = int(os.getenv('MIN_BALANCE'))
BUY_AMOUNT = int(os.getenv('BUY_AMOUNT'))
CHATID = os.getenv('CHATID')
X_CHECK_TOKEN = os.getenv('X_CHECK_TOKEN')
#MONGO_URL = os.getenv('MONGO_URL')
TELEGRAMTOKEN = os.getenv('TELEGRAMTOKEN')

#TelegramBot Connection
telegram_bot = telegram.Bot(TELEGRAMTOKEN)

# Create a new client and connect to the server
#client = MongoClient(MONGO_URL)

#exchange init
exchange = ccxt.binance({
    "apiKey": os.getenv("API_KEY"),
    "secret": os.getenv("API_SECRET"),
    "enableRateLimit": True,
    'options': {
    'defaultType': 'spot',
    },
})
exchange.set_sandbox_mode(True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Send a ping to confirm a successful connection
    try:
        #client.admin.command('ping')
        #print("Pinged your deployment. You successfully connected to MongoDB!")
        await telegram_bot.send_message(chat_id=CHATID, text='crypto-api Started!')
    except Exception as e:
        print(e)
    yield
    await exchange.close()
    await telegram_bot.send_message(chat_id=CHATID, text='crypto-api Closed!')
    await telegram_bot.close()
    
#Flask app
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Welcome to crypto-api"}

@app.get("/health-check")
async def hello():
    return {"status": "ok"}

@app.get('/balance/')
async def get_balance(base: Annotated[str | None, Query(max_length=10)] = None):
    try:
        balance = await exchange.fetch_balance()
        if not base:
            return {"balance" : balance['total']}
        base_balance = balance.get(base.upper())
        if not base_balance:
            raise HTTPException(status_code=404, detail="Base not found")
        return {"balance" : {base:base_balance}}
    except ccxt.NetworkError as e:
        raise HTTPException(status_code=502,detail='fetch_balance failed due to a network error: {}'.format(str(e)))
    except ccxt.ExchangeError as e:
        raise HTTPException(status_code=502,detail='fetch_balance failed due to exchange error:{}'.format(str(e)))
    except Exception as e:
        raise HTTPException(status_code=502,detail='fetch_balance failed with:{}'.format(str(e)))

class TradeSignal(BaseModel):
   x_check_token :str
   exchange :str = Field(title="The name of the exchange", max_length=20)
   position :str = Field(title="Position", max_length=10)
   trading_pair :str = Field(title="Trading pair", max_length=10)
   signal_price :str = Field(title="Signal price", max_length=25)
   balance_percent :str = Field(None, title="Balance percent value", max_length=3)

def validate_x_check_token(x_check_token):
    return True if x_check_token == X_CHECK_TOKEN else False

@app.post('/trade-signal')
async def trade(signal:TradeSignal):
    if not validate_x_check_token(signal.x_check_token):
        raise HTTPException(status_code=401, detail="Acess Denied")
    signal_price = float(signal.signal_price)
    balance = await exchange.fetch_balance()
    market = "/".join(signal.trading_pair.split(USDT)) + USDT
    try:
        match signal.position.upper():
            case "BUY":
                balance = balance[USDT]["free"]
                if MIN_BALANCE > balance:
                    raise Exception("Balance not suffisant.")
                buy_balance = BUY_AMOUNT
                if balance <= BUY_AMOUNT:
                    buy_balance = balance - MIN_BALANCE
                coin_count = buy_balance / signal_price
            case "SELL":
                base = signal.trading_pair.split(USDT)[0]
                balance = balance[base]["free"]
                if balance < 0:
                    raise Exception("Balance not suffisant")
                coin_count = balance
            case _:
                raise Exception("Bad Request(position)")
        if signal.balance_percent:
            coin_count = (buy_balance * (float(signal.balance_percent) / 100)) / signal_price
        await exchange.create_order(market, "limit", str(signal.position).lower(), coin_count, signal_price)
        text = f"{str(signal.position).upper()} order created::{coin_count} {market} from price {signal_price}"
        await telegram_bot.send_message(chat_id=CHATID, text=text)
        return {"signal_status": "Success"}
    except ccxt.NetworkError as e:
        raise HTTPException(status_code=400,detail='create_order failed due to a network error: {}'.format(str(e)))
    except ccxt.ExchangeError as e:
        raise HTTPException(status_code=400,detail='create_order failed due to exchange error:{}'.format(str(e)))
    except Exception as e:
        raise HTTPException(status_code=400,detail='create_order failed with:{}'.format(str(e)))