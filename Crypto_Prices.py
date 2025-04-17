# Crypto Price Tracker

from bs4 import BeautifulSoup
import time
import requests
import json
import os

# Load previous selection

def previous_selection():
    COINS_FILE = "coins.json"

    def load_coins():
        if os.path.exists(COINS_FILE):
            with open(COINS_FILE, "r") as file:
                return json.load(file)
        return []

    coins_data = load_coins()

    if not coins_data:
        print("\nNo previously saved coins found.")
        add_new = input("Would you like to add coins to track now? (y/n): ").lower()
        if add_new == 'y':
            return add_coins(coins_data)
        else:
            return []

    print("\nLoading previous selection and fetching prices:")
    prices_user_coins = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for coin_name in coins_data:
        coin_name = coin_name.strip().lower()
        url = f"https://coinmarketcap.com/currencies/{coin_name}/"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.find('span', class_='sc-65e7f566-0 WXGwg base-text', attrs={'data-test': 'text-cdp-price-display'})

            if price_element:
                price = price_element.text.strip()
                prices_user_coins[coin_name] = price
            else:
                prices_user_coins[coin_name] = "Price not found on CoinMarketCap"
                print(f"Price element not found for {coin_name.title()}!")

            time.sleep(1)

        except requests.exceptions.RequestException as e:
            prices_user_coins[coin_name] = f"Error fetching data from CoinMarketCap for {coin_name.title()}: {e}"
            print(f"Request Error for {coin_name.title()}: {e}")
        except Exception as e:
            prices_user_coins[coin_name] = f"An unexpected error occurred while fetching data from CoinMarketCap for {coin_name.title()}: {e}"
            print(f"Unexpected Error for {coin_name.title()}: {e}")

    for coin, price in prices_user_coins.items():
        print(f"{coin.title()}: {price}")

    while True:
        menu_or_refresh = input("\nMenu or Refresh? (m/r): ").lower()
        if menu_or_refresh == 'r':
            previous_selection()
            break
        elif menu_or_refresh == 'm':
            break
        else:
            print("Invalid choice. Please enter 'm' for Menu or 'r' for Refresh.")

    return coins_data

def add_coins(coins_data):
    new_coins = input("\nWhat coins would you like to add to track? (Comma-separated) ").split(",")
    new_coins = [coin.strip().lower() for coin in new_coins]
    coins_data.extend(new_coins)
    save_coins(coins_data)
    print(f"Coins '{', '.join(new_coins)}' added!")
    previous_selection()
    return coins_data

def save_coins(data):
    COINS_FILE = "coins.json"
    with open(COINS_FILE, "w") as file:
        json.dump(data, file, indent=4)

def previous_selection_load_only():
    COINS_FILE = "coins.json"
    if os.path.exists(COINS_FILE):
        with open(COINS_FILE, "r") as file:
            return json.load(file)
    return None

# Top 10

def top_10():
    top_10_coins = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get("https://coinmarketcap.com", headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        coin_rows = soup.find_all('tr', style='cursor:pointer')

        for i, row in enumerate(coin_rows[:10]):
            try:
                rank_element = row.find_all('td', style='text-align:start')[0].find('p', class_='sc-71024e3e-0 jBOvmG')
                rank = rank_element.text.strip() if rank_element else "N/A"

                name_element = row.find('p', class_='sc-65e7f566-0 iPbTJf coin-item-name')
                name = name_element.text.strip() if name_element else "N/A"

                price_td = row.find('td', style='text-align:end')
                price_element = price_td.find('span') if price_td else None
                price = price_element.text.strip() if price_element else "N/A"

                top_10_coins[rank] = {'name': name, 'price': price}

            except IndexError:
                print(f"Could not extract data from row {i+1}")
            except AttributeError as e:
                print(f"AttributeError while parsing row {i+1}: {e}")

        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinMarketCap: {e}")
    except Exception as e:
        print(f"An unexpected error occurred with CoinMarketCap: {e}")

    print("\nTop 10 Cryptocurrencies and their Prices (by Rank):\n")
    for rank, data in top_10_coins.items():
        print(f"{rank}: {data['name']} - {data['price']}")

    while True:
        menu_or_refresh = input("\nMenu or Refresh? (m/r): ").lower()
        if menu_or_refresh == 'r':
            top_50()  # Call top_50 again to refresh
            break
        elif menu_or_refresh == 'm':
            break
        else:
            print("Invalid choice. Please enter 'm' for Menu or 'r' for Refresh.")

# Top 50

def top_50():
    top_50_coins = {}
    url = "https://coinranking.com/coins"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        coin_rows = soup.find_all('tr', {'data-hx-boost': 'false'})

        print(f"Number of coin rows found: {len(coin_rows)}")

        for i, row in enumerate(coin_rows[:50]):
            try:
                rank_element = row.find('td', class_='semibold small align-center')
                rank = rank_element.text.strip() if rank_element else "N/A"

                name_element_anchor = row.find('a', class_='coin-profile')
                name_element_span = name_element_anchor.find('span', class_='coin-profile__name') if name_element_anchor else None
                name = name_element_span.text.strip() if name_element_span else "N/A"

                price_element = row.find('real-time-price')
                price = price_element.text.strip() if price_element else "N/A"

                top_50_coins[rank] = {'name': name, 'price': price}

            except IndexError:
                print(f"Could not extract data from row {i+1}")
            except AttributeError as e:
                print(f"AttributeError while parsing row {i+1}: {e}")

        print("\nTop 50 Cryptocurrencies and their Prices (by Rank):\n")
        for rank, data in top_50_coins.items():
            print(f"{rank}: {data['name']} - ${data['price']}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinRanking: {e}")
    except Exception as e:
        print(f"An unexpected error occurred with CoinRanking: {e}")

    while True:
        menu_or_refresh = input("\nMenu or Refresh? (m/r): ").lower()
        if menu_or_refresh == 'r':
            top_50()  # Call top_50 again to refresh
            break
        elif menu_or_refresh == 'm':
            break
        else:
            print("Invalid choice. Please enter 'm' for Menu or 'r' for Refresh.")

# Top 100

def top_100():
    top_100_coins = {}
    base_url = "https://coinranking.com/coins"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        for page_num in [1, 2]:
            url = f"{base_url}?page={page_num}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            coin_rows = soup.find_all('tr', {'data-hx-boost': 'false'})

            for i, row in enumerate(coin_rows):
                if len(top_100_coins) >= 100:
                    break  # Stop if we've collected 100 coins

                try:
                    rank_element = row.find('td', class_='semibold small align-center')
                    rank = rank_element.text.strip() if rank_element else "N/A"

                    name_element_anchor = row.find('a', class_='coin-profile')
                    name_element_span = name_element_anchor.find('span', class_='coin-profile__name') if name_element_anchor else None
                    name = name_element_span.text.strip() if name_element_span else "N/A"

                    price_element = row.find('real-time-price')
                    price = price_element.text.strip() if price_element else "N/A"

                    # Ensure rank is unique, though it should be based on the website's order
                    if rank not in top_100_coins:
                        top_100_coins[rank] = {'name': name, 'price': price}

                except IndexError:
                    print(f"Could not extract data from row {i+1} on page {page_num}")
                except AttributeError as e:
                    print(f"AttributeError while parsing row {i+1} on page {page_num}: {e}")

            time.sleep(1)  # Be polite and add a small delay between requests

        print("\nTop 100 Cryptocurrencies and their Prices (by Rank):\n")
        for rank, data in sorted(top_100_coins.items(), key=lambda item: int(item[0])):
            print(f"{rank}: {data['name']} - {data['price']}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinRanking: {e}")
    except Exception as e:
        print(f"An unexpected error occurred with CoinRanking: {e}")

    while True:
        menu_or_refresh = input("\nMenu or Refresh? (m/r): ").lower()
        if menu_or_refresh == 'r':
            top_100()  # Call top_100 again to refresh
            break
        elif menu_or_refresh == 'm':
            break
        else:
            print("Invalid choice. Please enter 'm' for Menu or 'r' for Refresh.")

# Input Coins to track

def user_coins():
    coins_to_track = input("\nWhat coins would you like to track? (Comma-separated) ").split(",")

    prices_user_coins = {}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for coin in coins_to_track:
        coin = coin.strip().lower()
        url = f"https://coinmarketcap.com/currencies/{coin}/"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')

            price_element = soup.find('span', class_='sc-65e7f566-0 WXGwg base-text', attrs={'data-test': 'text-cdp-price-display'})

            if price_element:
                price = price_element.text.strip()
                prices_user_coins[coin] = price
            else:
                prices_user_coins[coin] = "Price not found on CoinMarketCap"
                print("Price element not found on CoinMarketCap!")

            time.sleep(1)

        except requests.exceptions.RequestException as e:
            prices_user_coins[coin] = f"Error fetching data from CoinMarketCap: {e}"
            print(f"Request Error from CoinMarketCap: {e}")
        except Exception as e:
            prices_user_coins[coin] = f"An unexpected error occurred with CoinMarketCap: {e}"
            print(f"Unexpected Error with CoinMarketCap: {e}")

    for coin, price in prices_user_coins.items():
        print(f"\n{coin.title()}: {price}")

    while True:
        menu_or_refresh = input("\nMenu or Refresh? (m/r): ").lower()
        if menu_or_refresh == 'r':
            top_100()  # Call top_100 again to refresh
            break
        elif menu_or_refresh == 'm':
            break
        else:
            print("Invalid choice. Please enter 'm' for Menu or 'r' for Refresh.")

def remove_coins():
    COINS_FILE = "coins.json"

    def load_coins():
        if os.path.exists(COINS_FILE):
            with open(COINS_FILE, "r") as file:
                return json.load(file)
        return []

    coins_data = load_coins()

    coins_to_be_removed = [coin.strip().lower() for coin in input("\nWhat coins would you like to remove? ").split(",")]
    updated_coins_data = [coin for coin in coins_data if coin not in coins_to_be_removed]
    save_coins(updated_coins_data)
    print("\nCoins have been removed!")

# Menu Loop/ Coins to Track

while True:
    print("\nPlease select an option")
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
        top_10()
    elif choice == "3":
        top_50()
    elif choice == "4":
        top_100()
    elif choice == "5":
        user_coins()
    elif choice == "6":
        coins_data = previous_selection_load_only()
        if coins_data is None:
            coins_data = []
        add_coins(coins_data)
    elif choice == "7":
        remove_coins()
    elif choice == "8":
        print("\nGoodbye!")
        break
    else:
        print("\nInvalid choice, try again!")

