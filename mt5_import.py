import argparse
import logging
import sys
from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd
import pytz


TIMEFRAME_MAP = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
}


def parse_args():
    p = argparse.ArgumentParser(description="Fetch symbol data from MT5 and save to CSV")
    p.add_argument("-s", "--symbol", default="GBPNZD", help="Symbol to fetch (default: BTCUSD)")
    p.add_argument("-f", "--from", dest="utc_from", default="2023-01-01", help="Start date (YYYY-MM-DD) in UTC")
    p.add_argument("-t", "--to", dest="utc_to", default="2026-9-18", help="End date (YYYY-MM-DD) in UTC")
    p.add_argument("-r", "--timeframe", dest="timeframe", default="M15", choices=list(TIMEFRAME_MAP.keys()), help="Timeframe (M1,M5,M15,M30,H1,H4,D1)")
    p.add_argument("-o", "--outfile", default=None, help="Output CSV filename (default: SYMBOL_timeframe_from_to.csv)")
    p.add_argument("--terminal", default=None, help="Path to MetaTrader terminal executable (optional). Example: C:\\Program Files\\MetaTrader 5\\terminal64.exe")
    return p.parse_args()


def to_utc_dt(date_str):
    # Accept YYYY-MM-DD or YYYY-MM-DDTHH:MM formats
    try:
        dt = datetime.fromisoformat(date_str)
    except Exception:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    # attach UTC tz
    return dt.replace(tzinfo=pytz.timezone("Etc/UTC"))


def main():
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logging.info("Starting MT5 data fetch script")

    utc_from = to_utc_dt(args.utc_from)
    utc_to = to_utc_dt(args.utc_to)
    tf = TIMEFRAME_MAP[args.timeframe]

    logging.info("Initializing connection to MT5 terminal...")
    # Use provided terminal path if given (helps when multiple installations exist)
    if args.terminal:
        initialized = mt5.initialize(args.terminal)
    else:
        initialized = mt5.initialize()
    if not initialized:
        err = mt5.last_error()
        logging.error("initialize() failed, error=%s", err)
        sys.exit(1)

    try:
        try:
            info = mt5.terminal_info()
            logging.info("Connected to MT5 terminal: %s", info.product)
        except Exception:
            logging.info("Connected to MT5 terminal (no terminal info available)")

        logging.info("Fetching %s %s data from %s to %s", args.symbol, args.timeframe, utc_from.isoformat(), utc_to.isoformat())
        rates = mt5.copy_rates_range(args.symbol, tf, utc_from, utc_to)

        if rates is None or len(rates) == 0:
            logging.warning("No data retrieved. Tip: open MT5, go to View -> Symbols -> <symbol> -> Bars, and download data for the requested range.")
            return

        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df[['time', 'open', 'high', 'low', 'close']]
        df.rename(columns={'time': 'Timestamp', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, inplace=True)

        out = args.outfile or f"{args.symbol}_{args.timeframe}_{args.utc_from}_to_{args.utc_to}.csv"
        df.to_csv(out, index=False)
        logging.info("Success: data saved to %s", out)

    finally:
        try:
            mt5.shutdown()
            logging.info("MT5 shutdown completed")
        except Exception:
            logging.debug("Failed to shut down MT5 cleanly")


if __name__ == '__main__':
    main()
