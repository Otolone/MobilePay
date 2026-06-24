import os

from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from database.db import db

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.kyc_routes import kyc_bp
from routes.wallet_routes import wallet_bp
from routes.transaction_routes import transaction_bp
from routes.mtn_routes import mtn_bp
from routes.orange_routes import orange_bp
from routes.transfer_routes import transfer_bp
from routes.pawapay_routes import pawapay_bp



# Initialize extensions
jwt = JWTManager()

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {"success": False, "message": "Invalid token"}, 422

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {"success": False, "message": "Authorization token required"}, 401


app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs("uploads/kyc", exist_ok=True)

# Initialize DB + JWT
db.init_app(app)
jwt.init_app(app)


# Rate limiting
# Limits are defined per-route in routes/pawapay_routes.py.
# If flask-limiter is not installed, routes fall back to no limiting
# (the try/except in pawapay_routes.py handles this gracefully).
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter = Limiter(
        app=app, key_func=get_remote_address,
        default_limits=[],          # no global default; limits set per-route
        storage_uri="memory://",    # switch to "redis://..." in production
    )
except ImportError:
    pass  # Rate limiting disabled — install flask-limiter to enable


@app.route("/")
def home():
    return {"message": "MobilePay Backend Running"}


#Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(user_bp, url_prefix="/api/user")
app.register_blueprint(kyc_bp, url_prefix="/api/kyc")
app.register_blueprint(wallet_bp, url_prefix="/api/wallet")
app.register_blueprint(transaction_bp, url_prefix="/api/transactions")
app.register_blueprint(orange_bp, url_prefix="/api/orange")
app.register_blueprint(transfer_bp, url_prefix="/api/transfer")
app.register_blueprint(mtn_bp, url_prefix="/api/mtn")
app.register_blueprint(pawapay_bp, url_prefix="/api/pawapay")

with app.app_context():
    db.create_all()



if __name__ == "__main__":
    # debug=True must never be hardcoded — read from env var.
    # Set FLASK_DEBUG=true in .env for local development only.
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)