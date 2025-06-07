from flask import Flask
from flask_cors import CORS
from api.cases import bp as cases_bp
from api.precedents import bp as precedents_bp
from api.stats import bp as stats_bp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

app.register_blueprint(cases_bp)
app.register_blueprint(precedents_bp)
app.register_blueprint(stats_bp)

if __name__ == "__main__":
    app.run(debug=True)