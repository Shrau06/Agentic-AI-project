import yfinance as yf


def get_stock_info(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        return {
            "company_name": info.get("longName"),
            "symbol": info.get("symbol"),
            "current_price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "currency": info.get("currency"),
        }

    except Exception as e:
        return {"error": str(e)}


def get_price_history(symbol, period="1y"):
    """
    period:
    1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    """
    try:
        ticker = yf.Ticker(symbol)

        history = ticker.history(period=period)

        return history

    except Exception as e:
        print(e)
        return None


def get_daily_returns(symbol, period="1y"):
    try:
        ticker = yf.Ticker(symbol)

        history = ticker.history(period=period)

        history["Daily Return (%)"] = (
            history["Close"].pct_change() * 100
        )

        return history[
            ["Close", "Daily Return (%)"]
        ]

    except Exception as e:
        print(e)
        return None


def get_dividends(symbol):
    try:
        ticker = yf.Ticker(symbol)

        return ticker.dividends

    except Exception as e:
        print(e)
        return None


def get_volume_data(symbol, period="1y"):
    try:
        ticker = yf.Ticker(symbol)

        history = ticker.history(period=period)

        return history["Volume"]

    except Exception as e:
        print(e)
        return None


def get_company_summary(symbol):
    try:
        ticker = yf.Ticker(symbol)

        info = ticker.info

        return info.get(
            "longBusinessSummary",
            "Summary not available."
        )

    except Exception as e:
        return str(e)