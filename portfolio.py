import csv
from datetime import datetime

# Optional: Try importing yfinance for live data, otherwise use fallback pricing
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False


def get_current_price(ticker):
    """Fetches the current price of a stock using yfinance or falls back to a mock price dictionary."""
    if YFINANCE_AVAILABLE:
        try:
            stock = yf.Ticker(ticker)
            # Fetch latest close/current price
            todays_data = stock.history(period="1d")
            if not todays_data.empty:
                return float(todays_data["Close"].iloc[0])
        except Exception as e:
            print(f"Could not fetch live price for {ticker}: {e}")
    
    # Fallback sample prices if yfinance fails or is not installed
    fallback_prices = {
        "AAPL": 185.50,
        "MSFT": 420.00,
        "GOOGL": 175.25,
        "AMZN": 180.00,
        "TSLA": 170.50
    }
    return fallback_prices.get(ticker.upper(), 100.00)  # Default to 100 if unknown


def main():
    print("=== Stock Portfolio Performance Tracker ===")
    
    # Store portfolio positions in a dictionary structure
    # Format: { 'TICKER': {'shares': qty, 'buy_price': price} }
    portfolio = {}

    print("\nEnter your portfolio holdings. Type 'done' when finished.")
    while True:
        ticker = input("Enter stock ticker symbol (e.g., AAPL): ").strip().upper()
        if ticker == 'DONE':
            break
        if not ticker:
            print("Ticker cannot be empty. Try again.")
            continue

        try:
            shares = float(input(f"Enter number of shares for {ticker}: "))
            buy_price = float(input(f"Enter buy price per share for {ticker}: "))
        except ValueError:
            print("Invalid input for shares or price. Please enter numerical values.")
            continue

        portfolio[ticker] = {
            'shares': shares,
            'buy_price': buy_price
        }

    if not portfolio:
        print("No portfolio data entered. Exiting program.")
        return

    # Process and calculate metrics
    summary_data = []
    total_invested_capital = 0.0
    total_current_value = 0.0

    print("\nCalculating portfolio performance...")
    for ticker, data in portfolio.items():
        shares = data['shares']
        buy_price = data['buy_price']
        
        current_price = get_current_price(ticker)
        
        invested_capital = shares * buy_price
        current_market_value = shares * current_price
        gain_loss_dollar = current_market_value - invested_capital
        gain_loss_pct = (gain_loss_dollar / invested_capital) * 100 if invested_capital > 0 else 0.0

        total_invested_capital += invested_capital
        total_current_value += current_market_value

        summary_data.append({
            'Ticker': ticker,
            'Shares': shares,
            'Buy Price': round(buy_price, 2),
            'Current Price': round(current_price, 2),
            'Invested Capital': round(invested_capital, 2),
            'Current Value': round(current_market_value, 2),
            'Gain/Loss ($)': round(gain_loss_dollar, 2),
            'Gain/Loss (%)': round(gain_loss_pct, 2)
        })

    total_gain_loss_dollar = total_current_value - total_invested_capital
    total_gain_loss_pct = (total_gain_loss_dollar / total_invested_capital) * 100 if total_invested_capital > 0 else 0.0

    # Print Formatted Console Output
    print("\n" + "="*70)
    print(f"{'PORTFOLIO SUMMARY REPORT':^70}")
    print("="*70)
    print(f"{'Ticker':<8} {'Shares':<8} {'Buy ($)':<10} {'Current ($)':<12} {'Total Val ($)':<14} {'Gain/Loss (%)':<12}")
    print("-" * 70)
    
    for row in summary_data:
        print(f"{row['Ticker']:<8} {row['Shares']:<8} {row['Buy Price']:<10} {row['Current Price']:<12} {row['Current Value']:<14} {row['Gain/Loss (%)']:<12}%")
    
    print("-" * 70)
    print(f"Total Invested Capital: ${total_invested_capital:,.2f}")
    print(f"Total Current Value:    ${total_current_value:,.2f}")
    print(f"Total Gain/Loss:        ${total_gain_loss_dollar:,.2f} ({total_gain_loss_pct:.2f}%)")
    print("="*70)

    # Write results into 'portfolio_summary.csv' using Python's built-in csv module
    csv_filename = 'portfolio_summary.csv'
    fieldnames = ['Timestamp', 'Ticker', 'Shares', 'Buy Price', 'Current Price', 'Invested Capital', 'Current Value', 'Gain/Loss ($)', 'Gain/Loss (%)']
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in summary_data:
                row_with_time = {'Timestamp': timestamp, **row}
                writer.writerow(row_with_time)
        print(f"\nSuccessfully logged portfolio performance to '{csv_filename}'.")
    except IOError as e:
        print(f"\nError writing to CSV file: {e}")

if __name__ == "__main__":
    main()
