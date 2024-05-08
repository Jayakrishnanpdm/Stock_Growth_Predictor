from flask import Flask, request, render_template
from utils.prediction_utils import predict_stock, get_actual_and_predicted_data

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        if not (company := request.form.get("company", None)):
            return render_template("search.html", message="Failure")
        try:
            predicted_data = predict_stock(company)
            return render_template(
                "search.html",
                message="Success",
                close=predicted_data[0],
                open=predicted_data[1]['1. open'], 
                high=predicted_data[1]['2. high'], 
                low=predicted_data[1]['3. low'], 
                volume=predicted_data[1]['5. volume'],
            )
        except ValueError as e:
            return render_template("search.html", message="Failure")

    return render_template("search.html")

@app.route("/accuracy", methods=["POST"])
def accuracy():
    if not (model := request.form.get("model", None)):
        return render_template("accuracy.html", message="Failure")
    try:
        data = get_actual_and_predicted_data(model)
        return render_template(
            "accuracy.html",
            message="Success",
            mean_squared_error=data[0],
            data=data[1]
        )
    except ValueError as e:
        return render_template("accuracy.html", message="Failure")

if __name__ == "__main__":
    app.run(debug=True)
