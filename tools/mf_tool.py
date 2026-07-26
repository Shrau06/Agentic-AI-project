import requests
import pandas as pd

BASE_URL = "https://api.mfapi.in/mf"


def search_fund(fund_name):
    """
    Search mutual funds by name.

    Returns:
        [
            {
                "schemeCode": ...,
                "schemeName": ...
            }
        ]
    """

    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()

        funds = response.json()

        results = []

        for fund in funds:

            if fund_name.lower() in fund["schemeName"].lower():

                results.append(
                    {
                        "schemeCode": fund["schemeCode"],
                        "schemeName": fund["schemeName"]
                    }
                )

        return results[:10]

    except Exception as e:
        print(e)
        return []


def get_fund_details(scheme_code):
    """
    Fetch mutual fund details.

    Returns:
        {
            "scheme_name": ...,
            "fund_house": ...,
            "scheme_type": ...,
            "scheme_category": ...
        }
    """

    try:
        url = f"{BASE_URL}/{scheme_code}"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        meta = data.get("meta", {})

        return {
            "scheme_name": meta.get("scheme_name"),
            "fund_house": meta.get("fund_house"),
            "scheme_type": meta.get("scheme_type"),
            "scheme_category": meta.get("scheme_category")
        }

    except Exception as e:
        print(e)
        return None


def get_nav_history(scheme_code):
    """
    Returns NAV history as a DataFrame.
    """

    try:

        url = f"{BASE_URL}/{scheme_code}"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        nav_data = data.get("data", [])

        df = pd.DataFrame(nav_data)

        if df.empty:
            return None

        df["date"] = pd.to_datetime(
            df["date"],
            format="%d-%m-%Y"
        )

        df["nav"] = df["nav"].astype(float)

        df.sort_values(
            "date",
            inplace=True
        )

        return df

    except Exception as e:
        print(e)
        return None