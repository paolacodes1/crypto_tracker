import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import requests
from bs4 import BeautifulSoup
import time
import json
import os

class CryptoTrackerGUI:
    def __init__(self, window):
        self.window = window
        window.title("Crypto Price Tracker")
        self.coins_file = "coins.json"
        self.coins_data = self.load_coins()

        # --- Widgets ---
        self.title_label = tk.Label(window, text="Crypto Price Tracker", font=("Arial", 16))
        self.output_text = scrolledtext.ScrolledText(window, width=60, height=20)
        self.status_label = tk.Label(window, text="Ready")

        # --- Buttons ---
        self.load_button = tk.Button(window, text="Load Previous", command=self.load_previous_selection_gui)
        self.top10_button = tk.Button(window, text="Top 10", command=self.top_10_gui)
        self.top50_button = tk.Button(window, text="Top 50", command=self.top_50_gui)
        self.top100_button = tk.Button(window, text="Top 100", command=self.top_100_gui)
        self.add_button = tk.Button(window, text="Add Coins", command=self.add_coins_gui)
        self.remove_button = tk.Button(window, text="Remove Coins", command=self.remove_coins_gui)
        self.refresh_button = tk.Button(window, text="Refresh", command=self.refresh_gui)
        self.exit_button = tk.Button(window, text="Exit", command=window.quit)

        # --- Layout ---
        self.title_label.pack(pady=10)
        self.output_text.pack(padx=10, pady=10)
        self.load_button.pack(pady=5)
        self.top10_button.pack(pady=5)
        self.top50_button.pack(pady=5)
        self.top100_button.pack(pady=5)
        self.add_button.pack(pady=5)
        self.remove_button.pack(pady=5)
        self.refresh_button.pack(pady=5)
        self.exit_button.pack(pady=5)
        self.status_label.pack(pady=5)

    # --- Data Handling ---
    def load_coins(self):
        COINS_FILE = "coins.json"
        if os.path.exists(COINS_FILE):
            try:
                with open(COINS_FILE, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Error: coins.json is corrupted. Returning empty list.")
                return []
        return []

    def save_coins(self, data):
        COINS_FILE = "coins.json"
        try:
            with open(COINS_FILE, "w") as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            print(f"Error writing to coins.json: {e}")

    def fetch_prices(self, coins_list):
        prices_user_coins = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        for coin in coins_list:
            coin = coin.strip().lower()
            url = f"https://coinmarketcap.com/currencies/{coin}/"
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                price_element = soup.find('span', class_='sc-65e7f566-0 WXGwg base-text', attrs={'data-test': 'text-cdp-price-display'})
                if price_element:
                    prices_user_coins[coin] = price_element.text.strip()
                else:
                    prices_user_coins[coin] = "Price not found"
            except requests.exceptions.RequestException as e:
                prices_user_coins[coin] = f"Error: {e}"
            time.sleep(1)
        return prices_user_coins

    def top_10(self):
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
                except (IndexError, AttributeError) as e:
                    return f"Error extracting top 10 data: {e}"
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            return f"Error fetching top 10 data: {e}"
        return top_10_coins

    def top_50(self):
        top_50_coins = {}
        base_url = "https://coinranking.com/coins"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            coin_rows = soup.find_all('tr', {'data-hx-boost': 'false'})
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
                except (IndexError, AttributeError) as e:
                    return f"Error extracting top 50 data: {e}"
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            return f"Error fetching top 50 data: {e}"
        return top_50_coins

    def top_100(self):
        top_100_coins = {}
        base_url = "https://coinranking.com/coins"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        for page_num in [1, 2]:
            url = f"{base_url}?page={page_num}"
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                coin_rows = soup.find_all('tr', {'data-hx-boost': 'false'})
                for i, row in enumerate(coin_rows):
                    if len(top_100_coins) >= 100:
                        break
                    try:
                        rank_element = row.find('td', class_='semibold small align-center')
                        rank = rank_element.text.strip() if rank_element else "N/A"
                        name_element_anchor = row.find('a', class_='coin-profile')
                        name_element_span = name_element_anchor.find('span', class_='coin-profile__name') if name_element_anchor else None
                        name = name_element_span.text.strip() if name_element_span else "N/A"
                        price_element = row.find('real-time-price')
                        price = price_element.text.strip() if price_element else "N/A"
                        if rank not in top_100_coins:
                            top_100_coins[rank] = {'name': name, 'price': price}
                    except (IndexError, AttributeError) as e:
                        return f"Error extracting top 100 data on page {page_num}: {e}"
                time.sleep(1)
            except requests.exceptions.RequestException as e:
                return f"Error fetching top 100 data: {e}"
        return top_100_coins

    def user_coins(self, coins_to_track):
        prices_user_coins = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        for coin in coins_to_track:
            coin = coin.strip().lower()
            url = f"https://coinmarketcap.com/currencies/{coin}/"
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                price_element = soup.find('span', class_='sc-65e7f566-0 WXGwg base-text', attrs={'data-test': 'text-cdp-price-display'})
                if price_element:
                    prices_user_coins[coin] = price_element.text.strip()
                else:
                    prices_user_coins[coin] = "Price not found"
            except requests.exceptions.RequestException as e:
                prices_user_coins[coin] = f"Error: {e}"
            time.sleep(1)
        return prices_user_coins

    # --- GUI Interaction Functions ---
    def display_output(self, data):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and 'name' in value and 'price' in value:
                    self.output_text.insert(tk.END, f"{key}: {value['name']} - {value['price']}\n")
                else:
                    self.output_text.insert(tk.END, f"{key}: {value}\n")
        elif isinstance(data, list):
            for item in data:
                self.output_text.insert(tk.END, f"{item}\n")
        else:
            self.output_text.insert(tk.END, str(data) + "\n")
        self.output_text.config(state=tk.DISABLED)

    def update_status(self, message):
        self.status_label.config(text=message)
        self.window.update_idletasks()

    def load_previous_selection_gui(self):
        self.update_status("Loading previous selection...")
        self.coins_data = self.load_coins()
        if self.coins_data:
            prices = self.fetch_prices(self.coins_data)
            if isinstance(prices, dict):
                self.display_output(prices)
            else:
                self.display_output(prices)
            self.update_status("Previous selection loaded.")
        else:
            self.display_output("No previously saved coins found.")
            self.update_status("Ready.")

    def top_10_gui(self):
        self.update_status("Fetching top 10...")
        top_10_data = self.top_10()
        if isinstance(top_10_data, dict):
            self.display_output(top_10_data)
        else:
            self.display_output(top_10_data)
        self.update_status("Top 10 displayed.")

    def top_50_gui(self):
        self.update_status("Fetching top 50...")
        top_50_data = self.top_50()
        if isinstance(top_50_data, dict):
            self.display_output(top_50_data)
        else:
            self.display_output(top_50_data)
        self.update_status("Top 50 displayed.")

    def top_100_gui(self):
        self.update_status("Fetching top 100...")
        top_100_data = self.top_100()
        if isinstance(top_100_data, dict):
            self.display_output(top_100_data)
        else:
            self.display_output(top_100_data)
        self.update_status("Top 100 displayed.")

    def add_coins_gui(self):
        new_coins = simpledialog.askstring("Add Coins", "Enter coins to add (comma-separated):")
        if new_coins:
            coins_list = [coin.strip().lower() for coin in new_coins.split(',')]
            self.coins_data.extend(coins_list)
            self.save_coins(self.coins_data)
            messagebox.showinfo("Success", f"Coins '{', '.join(coins_list)}' added!")
            self.load_previous_selection_gui()

    def remove_coins_gui(self):
        coins_to_remove = simpledialog.askstring("Remove Coins", "Enter coins to remove (comma-separated):")
        if coins_to_remove:
            coins_list = [coin.strip().lower() for coin in coins_to_remove.split(',')]
            self.coins_data = [coin for coin in self.coins_data if coin not in coins_list]
            self.save_coins(self.coins_data)
            messagebox.showinfo("Success", "Coins removed.")
            self.load_previous_selection_gui()

    def refresh_gui(self):
        self.load_previous_selection_gui()  # For simplicity, just reload tracked coins

    def exit_gui(self):
        self.window.quit()

if __name__ == "__main__":
    window = tk.Tk()
    app = CryptoTrackerGUI(window)
    window.protocol("WM_DELETE_WINDOW", app.exit_gui)  # Handle window close event
    window.mainloop()
