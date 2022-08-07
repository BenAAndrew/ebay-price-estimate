MAX_DIFF = 2

def remove_outliers(items):
    prices = [i["price"] for i in items]
    average_price = sum(prices) / len(prices)
    min_price = average_price / MAX_DIFF
    max_price = average_price * MAX_DIFF
    return list(filter(lambda i: i["price"] >= min_price and i["price"] <= max_price, items))

def get_date_series(items, dates):
    date_values = [[i["price"] for i in items if i["date"] == date] for date in dates]
    return {
        "low": [min(i) for i in date_values],
        "avg": [sum(i) / len(i) for i in date_values],
        "high": [max(i) for i in date_values]
    }

def get_range(items):
    prices = [i["price"] for i in items]
    return {
        "low": min(prices),
        "high": max(prices)
    }

def get_volatility(items):
    prices = [i["price"] for i in items]
    average_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    min_diff = average_price - min_price
    max_diff = max_price - average_price
    diff = max(min_diff, max_diff)
    return diff / average_price
