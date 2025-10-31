import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env
load_dotenv()

# Pick config name from env (default = development)
config_name = os.getenv("FLASK_ENV", "development")

# Create Flask app with chosen config
app = create_app(config_name)

if __name__ == "__main__":
    # Run with host/port from env or defaults
    app.run(
        host= "127.0.0.1",
        port= 5000,
        debug=app.config["DEBUG"]
    )