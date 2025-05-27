from flask import Flask
from api.precedents import bp as precedents_bp

app = Flask(__name__)
app.register_blueprint(precedents_bp)

if __name__ == "__main__":
    app.run(debug=True)
