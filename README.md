<<<<<<< HEAD
# Trader_AngleOne

A lightweight, efficient Python wrapper for fetching historical equity market data via Angel One SmartAPI.

## Features

- **Easy Authentication:** Initialize seamlessly using dictionary unpacking.
- **Granular Timeframes:** Supports 1-minute up to daily data intervals.
- **NSE Equity Focus:** Built specifically to fetch NSE - EQ segment data (e.g., NIFTY, BANKNIFTY, RELIANCE, CIPLA).

---

## Installation

Install the package via pip (once published to PyPI):

```bash
pip install Trader_AngleOne
```

---

## Quick Start & Usage

This library focuses exclusively on the **NSE Equity (NSE-EQ)** segment. It does not support Derivatives/Futures data.

Here is how to initialize the trader and fetch historical data across various timeframes:

```python
from Trader_AngleOne import TraderAngleOne

# 1. Define your Angel One API credentials
crd = {
    "api_key"    : "abc",
    "secret_key" : "abc-abc-abc",
    "totp"       : "abcAKBDLEMI",
    "userid"     : "U8XX1XX",
    "pwd"        : "1XX8",
}

# 2. Initialize the client using dictionary unpacking
angle = TraderAngleOne(**crd)

# 3. Fetch Historical Data (Parameters: Token/Symbol, Interval, Start Time, End Time, Exchange)

# Fetch 1-Minute Data
reliance_1 = angle.get_history_data('RELIANCE', '1', '2026-01-01 9:15', '2026-01-02 15:30', 'NSE')

# Fetch 3-Minute Data
reliance_3 = angle.get_history_data('RELIANCE', '3', '2026-01-01 9:15', '2026-01-02 15:30', 'NSE')

# Fetch 5-Minute Data
reliance_5 = angle.get_history_data('RELIANCE', '5', '2026-01-01 9:15', '2026-01-02 15:30', 'NSE')

# Fetch 15-Minute Data
reliance_15 = angle.get_history_data('RELIANCE', '15', '2026-01-01 9:15', '2026-01-02 15:30', 'NSE')

# Fetch 30-Minute Data
reliance_30 = angle.get_history_data('RELIANCE', '30', '2026-01-01 9:15', '2026-01-02 15:30', 'NSE')

# Fetch 1-Hour Data
reliance_1H = angle.get_history_data('RELIANCE', '1H', '2026-01-01 9:15', '2026-01-02 15:30', 'NSE')

# Fetch 1-Day Data
reliance_1D = angle.get_history_data('RELIANCE', '1D', '2026-01-01 9:15', '2026-01-02 15:30', 'NSE')
```

---

## Supported Timeframes

Pass these exact string values into the second argument of `get_history_data()`:

- `"1"` - 1 Minute
- `"3"` - 3 Minutes
- `"5"` - 5 Minutes
- `"15"` - 15 Minutes
- `"30"` - 30 Minutes
- `"1H"` - 1 Hour
- `"1D"` - 1 Day

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
=======
# Trader_AngleOne
>>>>>>> d983ccc6afe5dd7c494481585c5374dd60606e58
