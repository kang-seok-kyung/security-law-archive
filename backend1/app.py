from flask import Flask
from flask_cors import CORS
from api.precedents import bp as precedents_bp
from ingest import collect_security_laws

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

app.register_blueprint(precedents_bp)

# 🔥 서버 실행 전 한 번 실행됨
collect_security_laws()

if __name__ == "__main__":
    app.run(debug=True)