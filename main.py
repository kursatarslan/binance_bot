# main.py

from fastapi import FastAPI, HTTPException, BackgroundTasks
from models import OrderRequest
from trade_bot import trade_bot, get_balance
from binance_client import client
import threading
import time

app = FastAPI()

bot_running = False
symbol = "BTCUSDT"
quantity = 0.001
rsi_buy_threshold = 30
rsi_sell_threshold = 70

@app.on_event("startup")
async def startup_event():
    global bot_running
    bot_running = True
    threading.Thread(target=trade_bot, args=(symbol, quantity, rsi_buy_threshold, rsi_sell_threshold)).start()
    threading.Thread(target=log_balance).start()

@app.on_event("shutdown")
def shutdown_event():
    global bot_running
    bot_running = False

@app.post("/buy")
async def buy_order(request: OrderRequest):
    try:
        order = client.order_market_buy(
            symbol=request.symbol,
            quantity=request.quantity
        )
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sell")
async def sell_order(request: OrderRequest):
    try:
        order = client.order_market_sell(
            symbol=request.symbol,
            quantity=request.quantity
        )
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/balance")
async def get_account_balance():
    try:
        balances = client.get_account()['balances']
        result = []
        for balance in balances:
            asset = balance['asset']
            free = float(balance['free'])
            locked = float(balance['locked'])
            if free > 0 or locked > 0:
                result.append({"asset": asset, "free": free, "locked": locked})
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def log_balance():
    while bot_running:
        get_balance()
        time.sleep(20)

# Ana programın çalıştırılması
if __name__ == "__main__":
    import uvicorn

    # FastAPI uygulamasını başlatma
    uvicorn.run(app, host="0.0.0.0", port=8000)
