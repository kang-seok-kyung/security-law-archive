from flask import Flask
from flask_cors import CORS
from ingest.ingest import update_precedents
from api.cases import bp as cases_bp
from api.precedents import bp as precedents_bp
from api.stats import bp as stats_bp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

app.register_blueprint(cases_bp)
app.register_blueprint(precedents_bp)
app.register_blueprint(stats_bp)

# 서버 실행 시 자동으로 판례 데이터 수집
if __name__ == "__main__":
    update_precedents()
    app.run()