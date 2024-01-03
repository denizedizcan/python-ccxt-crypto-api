# Crypto Trading API with FastAPI

## Overview

This repository contains a FastAPI-based crypto trading API that allows you to fetch account balances, perform health checks, and execute trading signals on the Binance exchange. The application integrates with the Binance API using the `ccxt` library and communicates trade signals via Telegram.

## Features

- **Balance Retrieval:** Get your account balances for various assets or a specific base asset.

- **Health Check Endpoint:** Verify the health of the API by checking its status.

- **Trade Signal Execution:** Execute buy or sell orders based on trade signals.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/denizedizcan/python-ccxt-crypto-api.git
cd python-ccxt-crypto-api
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Set environment variables:
Create a .env file in the root directory and add the following variables:

```plaintext
API_KEY=your_binance_api_key
API_SECRET=your_binance_api_secret
TELEGRAMTOKEN=your_telegram_bot_token
CHATID=your_telegram_chat_id
MIN_BALANCE=minimum_balance_required
BUY_AMOUNT=buy_amount
X_CHECK_TOKEN=your_custom_security_token
```
4. Run the FastAPI application:

```bash
uvicorn main:app --reload
```

## Endpoints

### 1. Root Endpoint:
- **Path:** `/`
- **Description:** Welcome message.

### 2. Health Check Endpoint:
- **Path:** `/health-check`
- **Description:** Verify the health of the API.

### 3. Balance Endpoint:
- **Path:** `/balance/`
- **Description:** Get account balances.
- **Parameters:**
  - `base` (optional): Get the balance for a specific base asset.

### 4. Trade Signal Endpoint:
- **Path:** `/trade-signal`
- **Method:** POST
- **Description:** Execute a trade signal.
- **Request Body Example:**
```json
  {
    "x_check_token": "your_custom_security_token",
    "exchange": "binance",
    "position": "buy",
    "trading_pair": "btcusdt",
    "signal_price": "50000",
    "balance_percent": "50"
  }
```
- **x_check_token:** Your custom security token.
- **exchange:** The name of the exchange (e.g., "binance").
- **position:** The position to take ("buy" or "sell").
- **trading_pair:** The trading pair for the signal (e.g., "btcusdt").
- **signal_price:** The price at which the signal is triggered.
- **balance_percent** (optional): Balance percent value (e.g., "50").

**Note:** Ensure you replace placeholder values with actual data. Adjust the endpoint URL according to your API deployment.

Feel free to experiment with different parameters based on your trading strategy.


## Disclaimer

**No Responsibility Accepted:**

This project and its associated codebase are provided "as is," without any warranty, express or implied. The creators and contributors of this project make no representations or warranties regarding the completeness, accuracy, reliability, suitability, or availability of the project or its contents. 

**Usage at Your Own Risk:**

The use of this software and any actions taken based on its content are at your own risk. The creators and contributors will not be liable for any direct, indirect, incidental, consequential, or other damages arising out of the use, misuse, or inability to use this project.

**No Financial Advice:**

This project does not provide financial advice or recommendations. Any trading or investment decisions made based on this project's code or information are solely your responsibility.

**No Obligation to Update:**

The creators and contributors are under no obligation to update or revise the project to reflect circumstances or events occurring after the initial release.

By using this project, you acknowledge and agree to these terms. If you do not agree with these terms, refrain from using or accessing the project.

**Note:** This disclaimer is intended for informational purposes only and does not replace legal advice. You are encouraged to seek legal counsel for specific legal matters related to the use of this project.
