from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from flask_swagger_ui import get_swaggerui_blueprint
import requests
from datetime import timedelta
import logging

# Initialize the Flask app
app = Flask(__name__)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "your-256-bit-secret"  # Use a secure key in production
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DSwallow:KwtA718*@dist-6-505.uopnet.plymouth.ac.uk/COMP2001_DSwallow?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Logging Configuration
logging.basicConfig(level=logging.DEBUG)

# Swagger UI setup
SWAGGER_URL = '/swagger'  # Swagger's UI endpoint
API_URL = '/static/swagger.json'  # Paths to swagger.json

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Defines the User model
class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'CW2'}  # Specifies schema

    email = db.Column(db.String(200), primary_key=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Admin or User

# Defines the Trail model matching CW2.Trail schema
class Trail(db.Model):
    __tablename__ = 'Trail'
    __table_args__ = {'schema': 'CW2'}  # Specifies schema

    TrailID = db.Column(db.String(20), primary_key=True, nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    Difficulty = db.Column(db.String(40), nullable=True)
    Length = db.Column(db.Float, nullable=True)
    TrailType = db.Column(db.String(40), nullable=True)
    Duration = db.Column(db.String(40), nullable=True)
    OwnerEmail = db.Column(db.String(200), nullable=False)
    Latitude = db.Column(db.Float, nullable=True)
    Longitude = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            "TrailID": self.TrailID,
            "Name": self.Name,
            "Description": self.Description,
            "Difficulty": self.Difficulty,
            "Length": self.Length,
            "TrailType": self.TrailType,
            "Duration": self.Duration,
            "OwnerEmail": self.OwnerEmail,
            "Latitude": self.Latitude,
            "Longitude": self.Longitude
        }

# Routes
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Trail API. Use /swagger to access API documentation."

# Authentication Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    response = requests.post("https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users",
                             json={"email": email, "password": password})

    if response.status_code == 200:
        response_data = response.json()
        if response_data[0] == "Verified":
            # Retrieve role from the database
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({"error": "User not found in the database"}), 404

            role = user.role
            access_token = create_access_token(identity=email, additional_claims={"role": role})
            return jsonify({"message": "Authentication successful", "role": role, "token": access_token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# CRUD Routes for Trails
@app.route('/trails', methods=['GET'])
@jwt_required(optional=True)
def get_trails():
    claims = get_jwt()
    if not claims or claims.get("role") not in ["Admin", "User"]:
        return jsonify({"error": "Unauthorized"}), 403

    trails = Trail.query.all()
    return jsonify([trail.to_dict() for trail in trails]), 200

@app.route('/trails/<string:trail_id>', methods=['GET'])
@jwt_required(optional=True)
def get_trail(trail_id):
    claims = get_jwt()
    if not claims or claims.get("role") not in ["Admin", "User"]:
        return jsonify({"error": "Unauthorized"}), 403

    trail = Trail.query.get(trail_id)
    if trail:
        return jsonify(trail.to_dict()), 200
    return jsonify({"error": "Trail not found"}), 404

@app.route('/trails', methods=['POST'])
@jwt_required()
def create_trail():
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    new_trail = Trail(**data)
    db.session.add(new_trail)
    db.session.commit()
    return jsonify(new_trail.to_dict()), 201

@app.route('/trails/<string:trail_id>', methods=['PUT'])
@jwt_required()
def update_trail(trail_id):
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Unauthorized"}), 403

    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"error": "Trail not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(trail, key):
            setattr(trail, key, value)

    db.session.commit()
    return jsonify(trail.to_dict()), 200

@app.route('/trails/<string:trail_id>', methods=['DELETE'])
@jwt_required()
def delete_trail(trail_id):
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Unauthorized"}), 403

    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"error": "Trail not found"}), 404

    db.session.delete(trail)
    db.session.commit()
    return jsonify({"message": "Trail deleted successfully"}), 200

# Error Handlers
@app.errorhandler(422)
def handle_unprocessable_entity(e):
    logging.error(f"422 Error Occurred: {e}")
    return jsonify({"error": "Unprocessable Entity", "details": str(e)}), 422

# Runs the app
if __name__ == '__main__':
    print("Trail API is running at http://127.0.0.1:5000")
    print("Swagger documentation available at http://127.0.0.1:5000/swagger")
    app.run(host='0.0.0.0', port=5000, debug=True)
