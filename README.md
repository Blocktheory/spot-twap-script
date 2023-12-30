# Multi-Exchange TWAP Trading Script

## Introduction
This script offers a sophisticated implementation of the Time-Weighted Average Price (TWAP) trading strategy, now supporting multiple cryptocurrency exchanges including Binance, Gate.io, and MEXC. It allows users to execute trades evenly distributed over a specified time across different platforms, minimizing market impact and offering more flexibility.

## Features
- Place TWAP orders on Binance, Gate.io, and MEXC's spot markets.
- Customize trade assets (e.g., BTC, ETH, SOL) on each exchange.
- Specify TWAP duration in hours.
- Execute orders at regular intervals.
- Enhanced support for multiple API key management.

## Prerequisites
- Python 3.x
- Accounts on Binance, Gate.io, MEXC (as per requirement).
- API keys and secrets for each exchange account.

## Installation
1. Clone the repository: 
git clone https://github.com/Blocktheory/spot-twap-script

1. Navigate to the project directory:
cd spot-twap-script

1. Install the required Python packages:
pip install -r requirements.txt

## Configuration
Set your exchange API keys and secrets as environment variables. Update the `.env` file with the following:

Copy or move a file .env.sample to .env
BINANCE_API_KEY=
BINANCE_API_SECRET=
GATE_API_KEY=
GATE_API_SECRET=
MEXC_API_KEY=
MEXC_API_SECRET=