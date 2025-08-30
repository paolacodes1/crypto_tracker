# Crypto Price Tracker v2 - CoinGecko API Version

import requests
import json
import os
import time
from typing import Dict, List, Optional, Union

class CoinGeckoAPI:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.rate_limit_delay = 2.0  # CoinGecko free tier: 50 calls/minute (increased for safety)
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make API request with rate limiting and error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            time.sleep(self.rate_limit_delay)
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None
    
    def get_coin_price(self, coin_id: str, vs_currency: str = "usd") -> Optional[Dict]:
        """Get current price for a single coin"""
        endpoint = "/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": vs_currency,
            "include_market_cap": True,
            "include_24hr_change": True
        }
        return self._make_request(endpoint, params)
    
    def get_multiple_coin_prices(self, coin_ids: List[str], vs_currency: str = "usd") -> Optional[Dict]:
        """Get current prices for multiple coins"""
        endpoint = "/simple/price"
        params = {
            "ids": ",".join(coin_ids),
            "vs_currencies": vs_currency,
            "include_market_cap": True,
            "include_24hr_change": True
        }
        return self._make_request(endpoint, params)
    
    def get_top_coins(self, limit: int = 100, vs_currency: str = "usd") -> Optional[List]:
        """Get top coins by market cap"""
        endpoint = "/coins/markets"
        params = {
            "vs_currency": vs_currency,
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False
        }
        return self._make_request(endpoint, params)
    
    def search_coin(self, query: str) -> Optional[Dict]:
        """Search for a coin by name or symbol"""
        endpoint = "/search"
        params = {"query": query}
        return self._make_request(endpoint, params)

class CryptoPriceTracker:
    def __init__(self):
        self.api = CoinGeckoAPI()
        self.coins_file = "coins_v2.json"
        
    def load_coins(self) -> List[str]:
        """Load saved coin IDs from file"""
        if os.path.exists(self.coins_file):
            try:
                with open(self.coins_file, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading coins file: {e}")
                return []
        return []
    
    def save_coins(self, coin_ids: List[str]) -> None:
        """Save coin IDs to file"""
        try:
            with open(self.coins_file, "w") as file:
                json.dump(coin_ids, file, indent=4)
        except IOError as e:
            print(f"Error saving coins file: {e}")
    
    def coin_name_to_id(self, coin_name: str) -> Optional[str]:
        """Convert coin name/symbol to CoinGecko ID"""
        search_result = self.api.search_coin(coin_name)
        if not search_result:
            return None
            
        coins = search_result.get("coins", [])
        if coins:
            # Return the first match (most relevant)
            return coins[0].get("id")
        return None
    
    def format_price(self, price_data: Dict, coin_id: str) -> str:
        """Format price data for display"""
        if coin_id not in price_data:
            return "Price not found"
            
        coin_data = price_data[coin_id]
        price = coin_data.get("usd", "N/A")
        change_24h = coin_data.get("usd_24h_change", 0)
        
        if isinstance(price, (int, float)):
            price_str = f"${price:,.2f}"
        else:
            price_str = str(price)
            
        if isinstance(change_24h, (int, float)):
            change_str = f" ({change_24h:+.2f}%)"
            return f"{price_str}{change_str}"
        
        return price_str
    
    def display_coins_data(self, coins_data: List[Dict]) -> None:
        """Display formatted coin data"""
        if not coins_data:
            print("No data available")
            return
            
        print(f"\n{'Rank':<6} {'Name':<20} {'Symbol':<8} {'Price':<15} {'24h Change':<12} {'Market Cap':<15}")
        print("-" * 85)
        
        for coin in coins_data:
            rank = coin.get("market_cap_rank", "N/A")
            name = coin.get("name", "N/A")[:19]
            symbol = coin.get("symbol", "N/A").upper()
            price = coin.get("current_price", 0)
            change_24h = coin.get("price_change_percentage_24h", 0)
            market_cap = coin.get("market_cap", 0)
            
            price_str = f"${price:,.2f}" if isinstance(price, (int, float)) else "N/A"
            change_str = f"{change_24h:+.2f}%" if isinstance(change_24h, (int, float)) else "N/A"
            
            if isinstance(market_cap, (int, float)) and market_cap > 0:
                if market_cap >= 1e12:
                    market_cap_str = f"${market_cap/1e12:.2f}T"
                elif market_cap >= 1e9:
                    market_cap_str = f"${market_cap/1e9:.2f}B"
                elif market_cap >= 1e6:
                    market_cap_str = f"${market_cap/1e6:.2f}M"
                else:
                    market_cap_str = f"${market_cap:,.0f}"
            else:
                market_cap_str = "N/A"
            
            print(f"{rank:<6} {name:<20} {symbol:<8} {price_str:<15} {change_str:<12} {market_cap_str:<15}")

def previous_selection():
    """Load and display previously saved coins"""
    tracker = CryptoPriceTracker()
    coin_ids = tracker.load_coins()
    
    if not coin_ids:
        print("\nNo previously saved coins found.")
        add_new = input("Would you like to add coins to track now? (y/n): ").lower()
        if add_new == 'y':
            return add_coins([])
        else:
            return []
    
    print("\nLoading previous selection and fetching prices:")
    
    price_data = tracker.api.get_multiple_coin_prices(coin_ids)
    if not price_data:
        print("Failed to fetch price data")
        return coin_ids
    
    print(f"\n{'Coin':<20} {'Price':<20}")
    print("-" * 40)
    
    for coin_id in coin_ids:
        formatted_price = tracker.format_price(price_data, coin_id)
        print(f"{coin_id.title():<20} {formatted_price:<20}")
    
    while True:
        menu_or_refresh = input("\nMenu or Refresh? (m/r): ").lower()
        if menu_or_refresh == 'r':
            previous_selection()
            break
        elif menu_or_refresh == 'm':
            break
        else:
            print("Invalid choice. Please enter 'm' for Menu or 'r' for Refresh.")
    
    return coin_ids

def add_coins(current_coins: List[str]) -> List[str]:
    """Add new coins to track"""
    tracker = CryptoPriceTracker()
    
    new_coins_input = input("\nWhat coins would you like to add to track? (Comma-separated names/symbols): ")
    new_coin_names = [coin.strip() for coin in new_coins_input.split(",")]
    
    new_coin_ids = []
    for coin_name in new_coin_names:
        coin_id = tracker.coin_name_to_id(coin_name)
        if coin_id:
            new_coin_ids.append(coin_id)
            print(f"Found: {coin_name} -> {coin_id}")
        else:
            print(f"Could not find coin: {coin_name}")
    
    if new_coin_ids:
        updated_coins = list(set(current_coins + new_coin_ids))  # Remove duplicates
        tracker.save_coins(updated_coins)
        print(f"Added {len(new_coin_ids)} coins!")
        previous_selection()
        return updated_coins
    else:
        print("No valid coins were added.")
        return current_coins

def remove_coins():
    """Remove coins from tracking list"""
    tracker = CryptoPriceTracker()
    coin_ids = tracker.load_coins()
    
    if not coin_ids:
        print("No coins to remove.")
        return
    
    print("\nCurrently tracked coins:")
    for i, coin_id in enumerate(coin_ids, 1):
        print(f"{i}. {coin_id}")
    
    coins_to_remove_input = input("\nWhat coins would you like to remove? (Comma-separated names): ")
    coins_to_remove_names = [coin.strip().lower() for coin in coins_to_remove_input.split(",")]
    
    coins_to_remove_ids = []
    for coin_name in coins_to_remove_names:
        # Try to find exact match or use name-to-id conversion
        if coin_name in coin_ids:
            coins_to_remove_ids.append(coin_name)
        else:
            coin_id = tracker.coin_name_to_id(coin_name)
            if coin_id and coin_id in coin_ids:
                coins_to_remove_ids.append(coin_id)
    
    if coins_to_remove_ids:
        updated_coins = [coin_id for coin_id in coin_ids if coin_id not in coins_to_remove_ids]
        tracker.save_coins(updated_coins)
        print(f"Removed {len(coins_to_remove_ids)} coins!")
    else:
        print("No matching coins found to remove.")

def top_coins(limit: int):
    """Display top coins by market cap"""
    tracker = CryptoPriceTracker()
    
    print(f"\nFetching top {limit} cryptocurrencies...")
    coins_data = tracker.api.get_top_coins(limit)
    
    if not coins_data:
        print("Failed to fetch top coins data")
        return
    
    print(f"\nTop {limit} Cryptocurrencies by Market Cap:")
    tracker.display_coins_data(coins_data)
    
    while True:
        menu_or_refresh = input("\nMenu or Refresh? (m/r): ").lower()
        if menu_or_refresh == 'r':
            top_coins(limit)
            break
        elif menu_or_refresh == 'm':
            break
        else:
            print("Invalid choice. Please enter 'm' for Menu or 'r' for Refresh.")

def user_coins():
    """Track user-specified coins"""
    tracker = CryptoPriceTracker()
    
    coins_input = input("\nWhat coins would you like to track? (Comma-separated names/symbols): ")
    coin_names = [coin.strip() for coin in coins_input.split(",")]
    
    coin_ids = []
    for coin_name in coin_names:
        coin_id = tracker.coin_name_to_id(coin_name)
        if coin_id:
            coin_ids.append(coin_id)
            print(f"Found: {coin_name} -> {coin_id}")
        else:
            print(f"Could not find coin: {coin_name}")
    
    if not coin_ids:
        print("No valid coins found.")
        return
    
    price_data = tracker.api.get_multiple_coin_prices(coin_ids)
    if not price_data:
        print("Failed to fetch price data")
        return
    
    print(f"\n{'Coin':<20} {'Price':<20}")
    print("-" * 40)
    
    for coin_id in coin_ids:
        formatted_price = tracker.format_price(price_data, coin_id)
        print(f"{coin_id.title():<20} {formatted_price:<20}")
    
    while True:
        menu_or_refresh = input("\nMenu or Refresh? (m/r): ").lower()
        if menu_or_refresh == 'r':
            user_coins()
            break
        elif menu_or_refresh == 'm':
            break
        else:
            print("Invalid choice. Please enter 'm' for Menu or 'r' for Refresh.")

def main():
    """Main menu loop"""
    print("Crypto Price Tracker v2 - CoinGecko API")
    print("=" * 40)
    
    while True:
        print("\nPlease select an option:")
        print("1. Load previous selection")
        print("2. Top 10")
        print("3. Top 50") 
        print("4. Top 100")
        print("5. Input your selection")
        print("6. Add coins to the previous selection")
        print("7. Remove coins from the previous selection")
        print("8. Exit")
        
        choice = input("\nEnter a number: ")
        
        if choice == "1":
            previous_selection()
        elif choice == "2":
            top_coins(10)
        elif choice == "3":
            top_coins(50)
        elif choice == "4":
            top_coins(100)
        elif choice == "5":
            user_coins()
        elif choice == "6":
            tracker = CryptoPriceTracker()
            current_coins = tracker.load_coins()
            add_coins(current_coins)
        elif choice == "7":
            remove_coins()
        elif choice == "8":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice, try again!")

if __name__ == "__main__":
    main()