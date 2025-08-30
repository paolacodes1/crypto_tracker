# 📈 Crypto Price Tracker

A Python-based cryptocurrency price tracking application with both web scraping and API-based versions.

## 🚀 Quick Start

Choose your preferred version:

- **v1 (Web Scraping)**: `python3 src/Crypto_Prices.py`
- **v2 (CoinGecko API)**: `python3 src/Crypto_Prices_v2.py`
- **GUI Version**: `python3 dashboard/Crypto_Prices_Interface_v1.py`

## 📋 Versions

### v1 - Web Scraping Version
Traditional approach using web scraping from CoinMarketCap and CoinRanking.

**Features:**
- Web scraping with BeautifulSoup
- Data from CoinMarketCap and CoinRanking
- Persistent storage in `coins.json`

**Pros:** No API limits  
**Cons:** Slower, fragile to website changes

### v2 - CoinGecko API Version ⭐ **Recommended**
Modern approach using the CoinGecko API for reliable data.

**Features:**
- CoinGecko API integration (no API key required)
- Rate limiting and error handling
- Enhanced data display with market cap and 24h changes
- Smart coin search (convert names/symbols to IDs)
- Separate data file `coins_v2.json`

**Pros:** Fast, reliable, rich data  
**Cons:** API rate limits (50 calls/minute)

## 📊 Features

### Core Functionality
- **Real-time Price Tracking**: Get current prices for any cryptocurrency
- **Top Rankings**: View top 10, 50, or 100 cryptocurrencies by market cap
- **Personal Watchlist**: Save, add, or remove coins from your tracking list
- **Persistent Storage**: Your coin selections are saved between sessions
- **Multiple Interfaces**: CLI and GUI options available

### v2 Enhanced Features
- **Market Data**: Price, market cap, 24-hour change percentage
- **Smart Search**: Find coins by name or symbol
- **Better Formatting**: Clean, organized data presentation
- **Error Recovery**: Robust handling of API failures and rate limits

## ⚙️ Installation

### Prerequisites
```bash
Python 3.6 or higher
```

### Dependencies

**For v1 (Web Scraping):**
```bash
pip install requests beautifulsoup4
```

**For v2 (API Version):**
```bash
pip install requests
```

**For GUI Version:**
```bash
pip install requests beautifulsoup4 tkinter
```

## 🖥️ Usage Examples

### Command Line Interface
```bash
# Run v2 (recommended)
python3 src/Crypto_Prices_v2.py

# Or run v1
python3 src/Crypto_Prices.py
```

### GUI Interface
```bash
python3 dashboard/Crypto_Prices_Interface_v1.py
```

### Sample Output (v2)
```
Rank   Name                 Symbol   Price           24h Change   Market Cap     
-------------------------------------------------------------------------------------
1      Bitcoin              BTC      $43,250.50      +2.45%       $845.2B        
2      Ethereum             ETH      $3,125.75       -1.20%       $375.8B        
3      XRP                  XRP      $2.15           +5.80%       $122.4B        
```

## 📁 Project Structure

```
crypto_tracker_git/
├── src/
│   ├── Crypto_Prices.py      # v1 - Web scraping version
│   └── Crypto_Prices_v2.py   # v2 - CoinGecko API version
├── dashboard/
│   └── Crypto_Prices_Interface_v1.py  # GUI version
├── coins.json                # v1 saved coins
├── coins_v2.json            # v2 saved coins
├── README.md
└── LICENSE
```

## 🔧 Configuration

### v1 Configuration
Uses web scraping with built-in delays and error handling.

### v2 Configuration
- **Rate Limiting**: 1.2 seconds between API calls
- **Free Tier**: 10,000-30,000 requests/month
- **No API Key Required**: Uses CoinGecko's free public API

## 🛡️ Error Handling

Both versions include comprehensive error handling:
- Network connectivity issues
- API rate limiting (v2)
- Invalid coin names/symbols
- Data parsing errors
- File I/O operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both v1 and v2 versions
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **v1**: Data from CoinMarketCap and CoinRanking websites
- **v2**: Powered by [CoinGecko API](https://www.coingecko.com/en/api)
- The interface was created using AI, with my prompts and source code as reference
- Built with Python and love ❤️




