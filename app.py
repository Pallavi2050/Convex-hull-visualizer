# app.py
from flask import Flask, render_template, request
from convex_hull import gift_wrapping_algorithm, graham_scan, divide_and_conquer, plot_convex_hull

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', points=None, hull=None, plot=None)

@app.route('/calculate_convex_hull', methods=['POST'])
def calculate_convex_hull():
    points_str = request.form['points']
    points = [tuple(map(int, p.split(','))) for p in points_str.split('\n') if p.strip()]

    algorithm = request.form['algorithm']
    hull = None
    if algorithm == 'gift_wrapping':
        hull = gift_wrapping_algorithm(points)
    elif algorithm == 'graham_scan':
        hull = graham_scan(points)
    elif algorithm == 'divide_and_conquer':
        hull = divide_and_conquer(points)

    plot = None
    if hull:
        plot = plot_convex_hull(points, hull, algorithm)

    return render_template('index.html', points=points, hull=hull, plot=plot)

if __name__ == '__main__':
    app.run(debug=True)
