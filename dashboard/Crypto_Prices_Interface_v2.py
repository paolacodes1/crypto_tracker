import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from Crypto_Prices_v2 import CoinGeckoAPI, CryptoPriceTracker

class CryptoTrackerGUIv2:
    def __init__(self, window):
        self.window = window
        window.title("Crypto Price Tracker v2 - CoinGecko API")
        window.geometry("900x600")
        
        self.tracker = CryptoPriceTracker()
        self.coins_data = self.tracker.load_coins()

        # --- Widgets ---
        self.title_label = tk.Label(window, text="Crypto Price Tracker v2 - CoinGecko API", 
                                   font=("Arial", 16, "bold"), fg="#2E8B57")
        self.output_text = scrolledtext.ScrolledText(window, width=110, height=25, 
                                                   font=("Courier New", 10))
        self.status_label = tk.Label(window, text="Ready", fg="#666666")

        # --- Button Frame ---
        self.button_frame = tk.Frame(window)
        
        # --- Buttons ---
        self.load_button = tk.Button(self.button_frame, text="Load Previous", 
                                   command=self.load_previous_selection_gui, bg="#4CAF50", fg="black", width=12)
        self.top10_button = tk.Button(self.button_frame, text="Top 10", 
                                    command=lambda: self.top_coins_gui(10), bg="#81C784", fg="black", width=12)
        self.top50_button = tk.Button(self.button_frame, text="Top 50", 
                                    command=lambda: self.top_coins_gui(50), bg="#64B5F6", fg="black", width=12)
        self.top100_button = tk.Button(self.button_frame, text="Top 100", 
                                     command=lambda: self.top_coins_gui(100), bg="#90CAF9", fg="black", width=12)
        self.add_button = tk.Button(self.button_frame, text="Add Coins", 
                                  command=self.add_coins_gui, bg="#FFB74D", fg="black", width=12)
        self.remove_button = tk.Button(self.button_frame, text="Remove Coins", 
                                     command=self.remove_coins_gui, bg="#F8BBD9", fg="black", width=12)
        self.search_button = tk.Button(self.button_frame, text="Search Coins", 
                                     command=self.search_coins_gui, bg="#CE93D8", fg="black", width=12)
        self.refresh_button = tk.Button(self.button_frame, text="Refresh", 
                                      command=self.refresh_gui, bg="#B0BEC5", fg="black", width=12)
        self.exit_button = tk.Button(self.button_frame, text="Exit", 
                                   command=window.quit, bg="#BCAAA4", fg="black", width=12)

        # --- Layout ---
        self.title_label.pack(pady=10)
        self.output_text.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)
        
        self.button_frame.pack(pady=10)
        
        # Pack buttons in rows
        self.load_button.grid(row=0, column=0, padx=5, pady=2)
        self.top10_button.grid(row=0, column=1, padx=5, pady=2)
        self.top50_button.grid(row=0, column=2, padx=5, pady=2)
        self.top100_button.grid(row=0, column=3, padx=5, pady=2)
        
        self.add_button.grid(row=1, column=0, padx=5, pady=2)
        self.remove_button.grid(row=1, column=1, padx=5, pady=2)
        self.search_button.grid(row=1, column=2, padx=5, pady=2)
        self.refresh_button.grid(row=1, column=3, padx=5, pady=2)
        
        self.exit_button.grid(row=2, column=1, columnspan=2, padx=5, pady=10)
        
        self.status_label.pack(pady=5)

        # Display welcome message
        self.display_welcome()

    def display_welcome(self):
        """Display welcome message with instructions"""
        welcome_msg = """
🚀 Welcome to Crypto Price Tracker v2!

This version uses the CoinGecko API for fast, reliable cryptocurrency data.

📊 Features:
• Real-time price tracking with 24h changes
• Market cap and ranking information  
• Smart coin search (by name or symbol)
• Personal watchlist management
• No API key required!

🔧 Instructions:
1. Click "Top 10/50/100" to view market rankings
2. Click "Search Coins" to find and track specific cryptocurrencies
3. Use "Add/Remove Coins" to manage your personal watchlist
4. Click "Load Previous" to view your saved coins

💡 Tip: Data updates every time you refresh or load new information.

Ready to track cryptocurrencies? Click any button above to start!
        """
        self.display_output(welcome_msg)

    def display_output(self, data):
        """Display data in the output text area"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            # Format coin data in a table - don't clear again, just format
            self.display_formatted_coins(data, clear_first=False)
        elif isinstance(data, dict):
            # Display dictionary data
            for key, value in data.items():
                if isinstance(value, dict) and 'name' in value and 'price' in value:
                    self.output_text.insert(tk.END, f"{key}: {value['name']} - {value['price']}\n")
                else:
                    self.output_text.insert(tk.END, f"{key}: {value}\n")
            self.output_text.config(state=tk.DISABLED)
        else:
            # Display string data
            self.output_text.insert(tk.END, str(data))
            self.output_text.config(state=tk.DISABLED)

    def display_formatted_coins(self, coins_data, clear_first=True):
        """Display formatted coin data in a table"""
        if clear_first:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete('1.0', tk.END)
            
        if not coins_data:
            self.output_text.insert(tk.END, "No data available\n")
            self.output_text.config(state=tk.DISABLED)
            return
        
        # Show count and header
        self.output_text.insert(tk.END, f"📊 Displaying {len(coins_data)} cryptocurrencies\n\n")
        
        # Header with better alignment using monospace formatting
        header = f"{'Rank':<4} {'Name':<20} {'Symbol':<8} {'Price':<15} {'24h Change':<12} {'Market Cap':<12}\n"
        separator = "=" * 78 + "\n"
        
        self.output_text.insert(tk.END, header)
        self.output_text.insert(tk.END, separator)
        
        for i, coin in enumerate(coins_data):
            try:
                rank = coin.get("market_cap_rank", i+1)
                name = coin.get("name", "N/A")[:19]  # Shorter for better alignment
                symbol = coin.get("symbol", "N/A").upper()
                price = coin.get("current_price", 0)
                change_24h = coin.get("price_change_percentage_24h", 0)
                market_cap = coin.get("market_cap", 0)
                
                # Format price
                price_str = f"${price:,.2f}" if isinstance(price, (int, float)) and price > 0 else "N/A"
                
                # Format 24h change
                if isinstance(change_24h, (int, float)):
                    change_str = f"{change_24h:+.2f}%"
                else:
                    change_str = "N/A"
                
                # Format market cap
                if isinstance(market_cap, (int, float)) and market_cap > 0:
                    if market_cap >= 1e12:
                        market_cap_str = f"${market_cap/1e12:.1f}T"
                    elif market_cap >= 1e9:
                        market_cap_str = f"${market_cap/1e9:.1f}B"
                    elif market_cap >= 1e6:
                        market_cap_str = f"${market_cap/1e6:.0f}M"
                    else:
                        market_cap_str = f"${market_cap:,.0f}"
                else:
                    market_cap_str = "N/A"
                
                line = f"{rank:<4} {name:<20} {symbol:<8} {price_str:<15} {change_str:<12} {market_cap_str:<12}\n"
                self.output_text.insert(tk.END, line)
                
            except Exception as e:
                self.output_text.insert(tk.END, f"Error displaying coin {i+1}: {str(e)}\n")
        
        # Now disable the text area
        self.output_text.config(state=tk.DISABLED)

    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.window.update_idletasks()

    def load_previous_selection_gui(self):
        """Load and display previously saved coins"""
        self.update_status("Loading previous selection...")
        self.coins_data = self.tracker.load_coins()
        
        if not self.coins_data:
            self.display_output("No previously saved coins found.\nUse 'Add Coins' or 'Search Coins' to start tracking cryptocurrencies!")
            self.update_status("No saved coins found.")
            return
        
        try:
            price_data = self.tracker.api.get_multiple_coin_prices(self.coins_data)
            if not price_data:
                self.display_output("Failed to fetch price data. Please try again.")
                self.update_status("API request failed.")
                return
            
            # Format the data for display
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete('1.0', tk.END)
            
            self.output_text.insert(tk.END, f"💰 Your Watchlist ({len(self.coins_data)} coins)\n\n")
            
            header = f"{'Coin':<20} {'Price':<20} {'24h Change':<12}\n"
            separator = "=" * 55 + "\n"
            
            self.output_text.insert(tk.END, header)
            self.output_text.insert(tk.END, separator)
            
            for coin_id in self.coins_data:
                formatted_price = self.tracker.format_price(price_data, coin_id)
                coin_name = coin_id.replace('-', ' ').title()
                # Parse the formatted price to separate price and 24h change  
                if " (" in formatted_price and ")" in formatted_price:
                    price_part = formatted_price.split(" (")[0]
                    change_part = "(" + formatted_price.split(" (")[1] 
                    line = f"{coin_name:<20} {price_part:<20} {change_part:<12}\n"
                else:
                    line = f"{coin_name:<20} {formatted_price:<20} {'N/A':<12}\n"
                self.output_text.insert(tk.END, line)
            
            self.output_text.config(state=tk.DISABLED)
            self.update_status(f"Loaded {len(self.coins_data)} saved coins.")
            
        except Exception as e:
            self.display_output(f"Error loading coins: {str(e)}")
            self.update_status("Error occurred.")

    def top_coins_gui(self, limit):
        """Fetch and display top coins"""
        self.update_status(f"Fetching top {limit} cryptocurrencies...")
        
        try:
            coins_data = self.tracker.api.get_top_coins(limit)
            if not coins_data:
                self.display_output("Failed to fetch top coins data. Please try again.")
                self.update_status("API request failed.")
                return
            
            self.display_formatted_coins(coins_data, clear_first=True)
            self.update_status(f"Displaying top {len(coins_data)} cryptocurrencies.")
            
        except Exception as e:
            self.display_output(f"Error fetching top coins: {str(e)}")
            self.update_status("Error occurred.")

    def search_coins_gui(self):
        """Search and track user-specified coins"""
        # Create custom dialog centered on main window
        dialog = tk.Toplevel(self.window)
        dialog.title("Search Coins")
        dialog.geometry("400x200")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center the dialog on the main window
        self.window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 200
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - 100
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Dialog content
        tk.Label(dialog, text="Enter coin names or symbols to search (comma-separated):", 
                font=("Arial", 10)).pack(pady=10)
        tk.Label(dialog, text="Examples: bitcoin, ethereum, cardano\nOr: BTC, ETH, ADA", 
                fg="gray").pack(pady=5)
        
        entry = tk.Entry(dialog, width=40, font=("Arial", 10))
        entry.pack(pady=10)
        entry.focus()
        
        result = {"coins_input": None}
        
        def on_ok():
            result["coins_input"] = entry.get()
            dialog.destroy()
            
        def on_cancel():
            dialog.destroy()
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="OK", command=on_ok, bg="#4CAF50", 
                 fg="black", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=on_cancel, bg="#F44336", 
                 fg="black", width=10).pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog to close
        dialog.wait_window()
        
        coins_input = result["coins_input"]
        if not coins_input:
            return
        
        self.update_status("Searching for coins...")
        coin_names = [coin.strip() for coin in coins_input.split(",")]
        
        found_coins = []
        search_results = ""
        
        for coin_name in coin_names:
            coin_id = self.tracker.coin_name_to_id(coin_name)
            if coin_id:
                found_coins.append(coin_id)
                search_results += f"✅ Found: {coin_name} → {coin_id}\n"
            else:
                search_results += f"❌ Could not find: {coin_name}\n"
        
        if not found_coins:
            self.display_output("No valid coins found. Please try different names or symbols.")
            self.update_status("No coins found.")
            return
        
        try:
            price_data = self.tracker.api.get_multiple_coin_prices(found_coins)
            if not price_data:
                self.display_output("Failed to fetch price data.")
                self.update_status("API request failed.")
                return
            
            # Display search results and prices
            output = "🔍 SEARCH RESULTS\n" + "=" * 50 + "\n\n"
            output += search_results + "\n"
            output += f"{'Coin':<25} {'Price':<20} {'24h Change':<12}\n"
            output += "-" * 60 + "\n"
            
            for coin_id in found_coins:
                formatted_price = self.tracker.format_price(price_data, coin_id)
                coin_name = coin_id.replace('-', ' ').title()
                output += f"{coin_name:<25} {formatted_price:<32}\n"
            
            self.display_output(output)
            self.update_status(f"Found {len(found_coins)} coins.")
            
        except Exception as e:
            self.display_output(f"Error fetching coin data: {str(e)}")
            self.update_status("Error occurred.")

    def add_coins_gui(self):
        """Add coins to watchlist"""
        # Create custom dialog centered on main window
        dialog = tk.Toplevel(self.window)
        dialog.title("Add Coins")
        dialog.geometry("400x200")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center the dialog
        self.window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 200
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - 100
        dialog.geometry(f"400x200+{x}+{y}")
        
        tk.Label(dialog, text="Enter coins to add to your watchlist (comma-separated):", 
                font=("Arial", 10)).pack(pady=10)
        tk.Label(dialog, text="Examples: bitcoin, ethereum, cardano", 
                fg="gray").pack(pady=5)
        
        entry = tk.Entry(dialog, width=40, font=("Arial", 10))
        entry.pack(pady=10)
        entry.focus()
        
        result = {"new_coins": None}
        
        def on_ok():
            result["new_coins"] = entry.get()
            dialog.destroy()
            
        def on_cancel():
            dialog.destroy()
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="OK", command=on_ok, bg="#4CAF50", 
                 fg="black", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=on_cancel, bg="#F44336", 
                 fg="black", width=10).pack(side=tk.LEFT, padx=5)
        
        dialog.wait_window()
        
        new_coins = result["new_coins"]
        if not new_coins:
            return
        
        self.update_status("Adding coins...")
        coin_names = [coin.strip() for coin in new_coins.split(',')]
        
        new_coin_ids = []
        for coin_name in coin_names:
            coin_id = self.tracker.coin_name_to_id(coin_name)
            if coin_id:
                new_coin_ids.append(coin_id)
        
        if new_coin_ids:
            updated_coins = list(set(self.coins_data + new_coin_ids))  # Remove duplicates
            self.tracker.save_coins(updated_coins)
            self.coins_data = updated_coins
            messagebox.showinfo("Success", f"Added {len(new_coin_ids)} coins to your watchlist!")
            self.load_previous_selection_gui()
        else:
            messagebox.showwarning("No Coins Added", "No valid coins were found.")
        
        self.update_status("Ready")

    def remove_coins_gui(self):
        """Remove coins from watchlist"""
        if not self.coins_data:
            messagebox.showinfo("No Coins", "No coins to remove.")
            return
        
        # Create custom dialog centered on main window
        dialog = tk.Toplevel(self.window)
        dialog.title("Remove Coins")
        dialog.geometry("450x300")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center the dialog
        self.window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 225
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - 150
        dialog.geometry(f"450x300+{x}+{y}")
        
        tk.Label(dialog, text="Currently tracked coins:", 
                font=("Arial", 11, "bold")).pack(pady=10)
        
        # Show current coins list
        coins_text = tk.Text(dialog, height=8, width=50, font=("Arial", 10))
        coins_text.pack(pady=5)
        for coin in self.coins_data:
            coins_text.insert(tk.END, f"• {coin.replace('-', ' ').title()}\n")
        coins_text.config(state=tk.DISABLED)
        
        tk.Label(dialog, text="Enter coins to remove (comma-separated):", 
                font=("Arial", 10)).pack(pady=(10,5))
        
        entry = tk.Entry(dialog, width=40, font=("Arial", 10))
        entry.pack(pady=5)
        entry.focus()
        
        result = {"coins_to_remove": None}
        
        def on_ok():
            result["coins_to_remove"] = entry.get()
            dialog.destroy()
            
        def on_cancel():
            dialog.destroy()
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="OK", command=on_ok, bg="#4CAF50", 
                 fg="black", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=on_cancel, bg="#F44336", 
                 fg="black", width=10).pack(side=tk.LEFT, padx=5)
        
        dialog.wait_window()
        
        coins_to_remove = result["coins_to_remove"]
        if not coins_to_remove:
            return
        
        coins_to_remove_names = [coin.strip().lower() for coin in coins_to_remove.split(',')]
        
        coins_to_remove_ids = []
        for coin_name in coins_to_remove_names:
            # Try exact match first
            if coin_name in self.coins_data:
                coins_to_remove_ids.append(coin_name)
            else:
                # Try name-to-id conversion
                coin_id = self.tracker.coin_name_to_id(coin_name)
                if coin_id and coin_id in self.coins_data:
                    coins_to_remove_ids.append(coin_id)
        
        if coins_to_remove_ids:
            updated_coins = [coin_id for coin_id in self.coins_data if coin_id not in coins_to_remove_ids]
            self.tracker.save_coins(updated_coins)
            self.coins_data = updated_coins
            messagebox.showinfo("Success", f"Removed {len(coins_to_remove_ids)} coins from your watchlist!")
            self.load_previous_selection_gui()
        else:
            messagebox.showwarning("No Coins Removed", "No matching coins found to remove.")

    def refresh_gui(self):
        """Refresh current view"""
        if self.coins_data:
            self.load_previous_selection_gui()
        else:
            self.display_welcome()

if __name__ == "__main__":
    window = tk.Tk()
    app = CryptoTrackerGUIv2(window)
    window.protocol("WM_DELETE_WINDOW", app.window.quit)
    window.mainloop()