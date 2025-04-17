# Crypto Price Tracker

## Description
The Crypto Price Tracker is a Python-based program that allows users to track cryptocurrency prices. It provides multiple functionalities including:

- Viewing the current price of individual or multiple cryptocurrencies.
- Accessing the top 10, top 50, and top 100 cryptocurrencies by market rank.
- Saving a list of user-selected cryptocurrencies for future tracking.
- Adding and removing coins from the list of tracked cryptocurrencies.

## Features

- **Track Cryptocurrency Prices**: Get real-time prices for any coin by entering its name.
- **Top 10, 50, 100 Cryptocurrencies**: Fetch the latest rankings and prices from CoinMarketCap and CoinRanking.
- **User Coin Selection**: Save, add, or remove cryptocurrencies to/from the list of tracked coins.
- **Persistent Storage**: The list of user-selected coins is saved in a `coins.json` file for future use.

## Requirements

Python 3.6 or higher
requests library
beautifulsoup4 library

## Dependencies

requests: To make HTTP requests to CoinMarketCap and CoinRanking websites.
beautifulsoup4: To parse HTML data and extract the cryptocurrency prices.
json: To read/write user coin data to a file.
License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

The prices and rankings are fetched from CoinMarketCap and CoinRanking websites.




