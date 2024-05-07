from flask import Flask, request, render_template

from utils.types import DatasetPath
from utils.prediction_utils import StockPredictor
app = Flask(__name__)


stock_predictor = StockPredictor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if not (company := request.form.get('company', None)):
            return render_template('search.html', message="Failure")
        if company == "tesla":
            predicted_data = stock_predictor.all_operations(DatasetPath.TESLA.value)
        elif company == "amazon":
            predicted_data = stock_predictor.all_operations(DatasetPath.AMAZON.value)
        else:
            predicted_data = "No Data Found"
        return render_template('search.html', message="Success", prediction=predicted_data[0])

    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
