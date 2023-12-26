# Binance TWAP Trading Script

## Introduction
This script provides a basic implementation of a Time-Weighted Average Price (TWAP) trading strategy for the Binance cryptocurrency exchange. It allows users to execute trades evenly distributed over a specified time, minimizing the market impact.

## Features
- Place TWAP orders on Binance's spot market
- Customize trade assets (e.g., BTC, ETH, SOL)
- Specify TWAP duration in hours
- Execute orders at regular intervals

## Prerequisites
- Python 3.x
- Binance account
- Binance API key and secret

## Installation
1. Clone the repository: 
git clone https://github.com/Blocktheory/bnc-twap-script

1. Navigate to the project directory:
cd [project directory]

1. Install the required Python packages:
pip install -r requirements.txt

## Configuration
Set your Binance API key and secret as environment variables:

Copy or move a file .env.sample to .env

BINANCE_API_KEY='your_api_key'
BINANCE_API_SECRET='your_api_secret'