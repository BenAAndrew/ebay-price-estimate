from ebay import build_url, get_items
from flask import Flask, render_template, request
from main import items
from analysis import get_date_series, get_range, get_volatility, remove_outliers

app = Flask(__name__, template_folder="static")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_dataset():
    url = build_url(request.form["search"], request.form["condition"])
    # items = get_items(url, include_delivery_price=False)
    # items = remove_outliers(items)

    dates = sorted(set([i["date"] for i in items]))
    prices = [i["price"] for i in items]
    average_price = sum(prices) / len(prices)
    graph = get_date_series(items, dates)
    range = get_range(items)
    volatility = get_volatility(items)
    formatted_dates = [d.strftime("%Y-%m-%d") for d in dates]
    return render_template(
        "out.html",
        dates=formatted_dates,
        average_price=average_price,
        graph=graph,
        range=range,
        volatility=volatility,
        sales=len(items),
    )


if __name__ == "__main__":
    app.run(debug=False)
