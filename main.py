from ebay import build_url, get_items, remove_outliers



url = build_url("rtx 3060", "used")
items = get_items(url)
items = remove_outliers(items)
prices = [i["price"] for i in items]
dates = [i["date"] for i in items]

print(min(prices), sum(prices) / len(prices), max(prices))
print(items)