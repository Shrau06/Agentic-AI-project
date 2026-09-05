from tools.mf_tool import search_fund

funds = search_fund("Parag")

for fund in funds:
    print(fund)

from tools.mf_tool import get_fund_details

details = get_fund_details(122639)

print(details)   

from tools.mf_tool import get_nav_history

df = get_nav_history(122639)

print(df.head())