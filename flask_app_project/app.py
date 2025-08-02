# import os
# from flask import Flask, request, jsonify, session, render_template # render_template is now correctly imported
# from flask_cors import CORS
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
# from dotenv import load_dotenv
# import bcrypt
# from bson.objectid import ObjectId
#
# # Load environment variables from .env file
# load_dotenv()
#
# app = Flask(__name__)
#
# # Flask needs a secret key for session management (essential for login security)
# app.secret_key = os.getenv("FLASK_SECRET_KEY", "a_very_secret_key_for_dev_change_me_in_production_12345")
#
# # Enable CORS for all routes. In production, you might want to restrict this
# # to specific frontend origins for security.
# CORS(app)
#
# # --- MongoDB Connection Setup ---
# MONGO_URI = os.getenv("MONGO_URI")
# # Database and collection for user signups/logins
# USER_DB_NAME = os.getenv("DATABASE_NAME", "register_signup")
# USER_COLLECTION_NAME = os.getenv("COLLECTION_NAME", "signup")
#
# # Ensure MONGO_URI is set
# if not MONGO_URI:
#     raise ValueError("MONGO_URI environment variable not set. Please check your .env file.")
#
# # Initialize MongoDB client
# client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
#
# # Get references to the collections
# db_users = client[USER_DB_NAME]
# signup_collection = db_users[USER_COLLECTION_NAME]
#
# # Test the MongoDB connection when the Flask app starts
# try:
#     client.admin.command('ping')
#     print("Successfully connected to MongoDB!")
# except Exception as e:
#     # IMPORTANT: Do NOT use exit(1) here in a production web server setup
#     # Gunicorn expects your app to stay running.
#     # If the database connection is critical, logging is usually sufficient,
#     # and external health checks (like Fly.io's) will mark the app unhealthy.
#     print(f"Failed to connect to MongoDB on startup: {e}")
#     # Consider raising an exception here if the app absolutely cannot function without DB.
#     # For now, we'll let it try to start, but subsequent DB operations might fail.
#
# # --- API Routes ---
#
# @app.route('/')
# def home():
#     """
#     Renders the main index.html page.
#     """
#     # Corrected typo: render_templste -> render_template
#     return render_template('index.html')
#
# @app.route('/register', methods=['POST'])
# def register_user():
#     """
#     Handles user registration. Expects username, email, and password.
#     Hashes password and stores user in MongoDB.
#     """
#     data = request.get_json()
#
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')
#
#     if not username or not email or not password:
#         return jsonify({"message": "Username, email, and password are required"}), 400
#
#     if signup_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
#         return jsonify({"message": "Username or email already exists"}), 409
#
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#
#     new_user = {
#         "username": username,
#         "email": email, # Corrected: removed duplicate 'email' field
#         "password": hashed_password
#     }
#
#     signup_collection.insert_one(new_user)
#
#     return jsonify({"message": "Account created successfully"}), 201
#
#
# @app.route('/login', methods=['POST'])
# def login_user():
#     """
#     Handles user login. Expects username/email and password.
#     Verifies credentials and sets up a session for the user.
#     """
#     data = request.get_json()
#
#     username_or_email = data.get('username_or_email')
#     password = data.get('password')
#
#     if not username_or_email or not password:
#         return jsonify({"message": "Username/Email and password are required"}), 400
#
#     user = signup_collection.find_one({
#         "$or": [
#             {"username": username_or_email},
#             {"email": username_or_email}
#         ]
#     })
#
#     if not user:
#         return jsonify({"message": "Invalid credentials"}), 401
#
#     if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
#         session['user_id'] = str(user['_id'])
#         session['username'] = user['username']
#
#         return jsonify({"message": "Login successful", "username": user['username']}), 200
#     else:
#         return jsonify({"message": "Invalid credentials"}), 401
#
#
# @app.route('/logout', methods=['POST'])
# def logout_user():
#     """
#     Logs out the current user by clearing their session data.
#     """
#     session.pop('user_id', None)
#     session.pop('username', None)
#     return jsonify({"message": "Logged out successfully"}), 200
#
#
# @app.route('/status', methods=['GET'])
# def get_login_status():
#     """
#     Returns the current login status of the user based on session data.
#     """
#     if 'user_id' in session:
#         return jsonify({"logged_in": True, "username": session['username']}), 200
#     else:
#         return jsonify({"logged_in": False}), 200
#
# # Removed @app.route('/schedule-demo', methods=['POST']) as Calendly handles this.
#
# # --- Main entry point for running the Flask app ---
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)






from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os # Don't forget to import os to access environment variables

app = Flask(__name__)
bcrypt = Bcrypt(app)

# --- MongoDB Configuration ---
# IMPORTANT: These values are read from environment variables set in your deployment environment!
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not MONGO_URI:
    print("ERROR: MONGO_URI environment variable not set. Please configure it for deployment!")
    # If MONGO_URI isn't set, try to connect to a local MongoDB as a fallback (for local development)
    # This will likely cause issues if your database isn't running locally when deployed.
    client = MongoClient('mongodb://localhost:27017/')
else:
    client = MongoClient(MONGO_URI)

# Ensure database and collection names are defined from environment variables
if not DATABASE_NAME or not COLLECTION_NAME:
    print("ERROR: DATABASE_NAME or COLLECTION_NAME environment variables not set. Cannot proceed with MongoDB connection.")
    # Fallback to default if not set (could lead to unexpected behavior if not intentional)
    db = client.get_default_database()
    users_collection = db.get_collection("users")
else:
    db = client[DATABASE_NAME]
    users_collection = db[COLLECTION_NAME]

# Test MongoDB connection at startup (useful for debugging deployment issues)
try:
    client.admin.command('ping')
    print("DEBUG: Successfully connected to MongoDB!")
except Exception as e:
    print(f"ERROR: Could not connect to MongoDB at startup: {e}")
    # In a production setup, you might want to consider exiting here if the DB connection is critical.
    # import sys
    # sys.exit(1)

# --- Streamlit App URL Configuration ---
# IMPORTANT: Replace this with the actual URL of your deployed Streamlit app!
STREAMLIT_APP_URL = "https://ancient-frost-8375.fly.dev/"

# Route for the home page, to serve your index.html
@app.route('/')
def serve_index():
    return render_template('index.html')

# Route to handle user signup (POST request)
@app.route('/signup', methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"error": "Missing username, email, or password"}), 400

    # Check if user already exists (by username or email)
    if users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
        return jsonify({"error": "Username or email already exists"}), 409 # 409 Conflict

    # Hash the password before storing it
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        # Insert the new user into the MongoDB collection
        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password # Storing the hashed password
        })
        print(f"DEBUG: User '{username}' signed up and saved to MongoDB.")
        return jsonify({"message": "Account created successfully!"}), 200
    except Exception as e:
        print(f"ERROR: Failed to save user to MongoDB: {e}")
        return jsonify({"error": "An internal server error occurred during signup."}), 500

# Route to handle user login (POST request)
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    username_or_email = data.get('username_or_email')
    password = data.get('password')

    if not all([username_or_email, password]):
        return jsonify({"error": "Missing username/email or password"}), 400

    # Find the user by username OR email in MongoDB
    user = users_collection.find_one({"$or": [
        {"username": username_or_email},
        {"email": username_or_email}
    ]})

    if user:
        # User found, now check the password
        if bcrypt.check_password_hash(user['password'], password):
            print(f"DEBUG: User '{username_or_email}' logged in successfully.")
            # If login is successful, tell the frontend to redirect to /platform
            return jsonify({"message": "Login successful!", "redirect_url": "/platform"}), 200
        else:
            # Password mismatch
            print(f"DEBUG: Login failed for '{username_or_email}': Incorrect password.")
            return jsonify({"error": "Invalid username/email or password"}), 401 # 401 Unauthorized
    else:
        # User not found
        print(f"DEBUG: Login failed for '{username_or_email}': User not found.")
        return jsonify({"error": "Invalid username/email or password"}), 401 # 401 Unauthorized

# NEW ROUTE: Handles the /platform request and redirects to your Streamlit app
@app.route('/platform')
def platform_redirect():
    # You might want to add an authentication check here in a real application
    # to ensure only truly logged-in users can access the Streamlit app.
    # For now, it performs a direct redirect.
    print(f"DEBUG: Redirecting to Streamlit app at: {STREAMLIT_APP_URL}")
    return redirect(STREAMLIT_APP_URL, code=302) # 302 Found is a standard temporary redirect

if __name__ == '__main__':
    # Use the PORT environment variable provided by deployment platforms (like Fly.io)
    # Default to port 5000 if PORT is not set (useful for local development).
    port = int(os.environ.get("PORT", 5000))
    # Bind to 0.0.0.0 to allow connections from outside the localhost, essential for containers.
    app.run(debug=True, host='0.0.0.0', port=port)

