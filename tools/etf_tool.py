import yfinance as yf


def get_etf_info(symbol):
    try:

        ticker = yf.Ticker(symbol)

        info = ticker.info

        return {
            "etf_name": info.get("longName"),
            "symbol": info.get("symbol"),
            "current_price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "expense_ratio": info.get("annualReportExpenseRatio"),
            "category": info.get("category"),
            "fund_family": info.get("fundFamily"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "currency": info.get("currency"),
        }

    except Exception as e:
        return {"error": str(e)}


def get_etf_history(symbol, period="1y"):
    """
    period:
    1mo, 3mo, 6mo, 1y, 2y, 5y, max
    """

    try:

        ticker = yf.Ticker(symbol)

        history = ticker.history(period=period)

        return history

    except Exception as e:
        print(e)
        return None


def get_etf_dividends(symbol):

    try:

        ticker = yf.Ticker(symbol)

        return ticker.dividends

    except Exception as e:
        print(e)
        return None


def get_etf_summary(symbol):

    try:

        ticker = yf.Ticker(symbol)

        info = ticker.info

        return info.get(
            "longBusinessSummary",
            "Summary not available."
        )

    except Exception as e:
        return str(e)


def get_etf_daily_returns(symbol, period="1y"):

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


def get_etf_volume(symbol, period="1y"):

    try:

        ticker = yf.Ticker(symbol)

        history = ticker.history(period=period)

        return history["Volume"]

    except Exception as e:
        print(e)
        return None