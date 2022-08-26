from ebay import build_url, get_items
from flask import Flask, render_template, request
from analysis import get_date_series, get_volatility, remove_outliers

app = Flask(__name__, template_folder="static")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_dataset():
    url = build_url(request.form["search"], request.form["condition"])
    items = get_items(url, include_delivery_price=False)

    if len(items) < 10:
        return render_template("index.html", error="Insufficent items found")

    items = remove_outliers(items)
    dates = sorted(set([i["date"] for i in items]))
    prices = [i["price"] for i in items]
    min_price = min(prices)
    average_price = sum(prices) / len(prices)
    max_price = max(prices)
    graph = get_date_series(items, dates)
    volatility = get_volatility(min_price, average_price, max_price)
    formatted_dates = [d.strftime("%Y-%m-%d") for d in dates]
    return render_template(
        "out.html",
        dates=formatted_dates,
        average_price=average_price,
        low=min_price,
        high=max_price,
        graph=graph,
        volatility=volatility,
        sales=len(items),
    )


if __name__ == "__main__":
    app.run(debug=False)
