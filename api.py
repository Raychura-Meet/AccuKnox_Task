from flask import Flask, jsonify

app = Flask(__name__)

# -------------------------------
# BOOKS API 
# -------------------------------
@app.route('/books')
def books():
    return jsonify([
        {"title": "AI Revolution", "author": "John Smith", "year": 2020},
        {"title": "Deep Learning", "author": "Ian Goodfellow", "year": 2016},
        {"title": "Machine Learning Basics", "author": "Tom Mitchell", "year": 1997},
        {"title": "Pattern Recognition", "author": "Christopher Bishop", "year": 2006},
        {"title": "Python Programming", "author": "Guido Rossum", "year": 2010},
        {"title": "Data Science Handbook", "author": "Jake VanderPlas", "year": 2016},
        {"title": "Artificial Intelligence", "author": "Stuart Russell", "year": 2010},
        {"title": "Neural Networks", "author": "Michael Nielsen", "year": 2015},
        {"title": "Computer Vision", "author": "Richard Szeliski", "year": 2011},
        {"title": "Natural Language Processing", "author": "Daniel Jurafsky", "year": 2008}
    ])

# -------------------------------
# STUDENTS API 
# -------------------------------
@app.route('/students')
def students():
    return jsonify([
        {"name": "Meet", "score": 95},
        {"name": "Rahul", "score": 78},
        {"name": "Amit", "score": 92},
        {"name": "Neha", "score": 88},
        {"name": "Priya", "score": 85},
        {"name": "Karan", "score": 81},
        {"name": "Simran", "score": 89},
        {"name": "Anjali", "score": 76},
        {"name": "Rohit", "score": 84},
        {"name": "Sneha", "score": 91}
    ])

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)