from dotenv import load_dotenv
load_dotenv()
import os
import shutil
from app import create_app

if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
    shutil.rmtree(os.environ["PROMETHEUS_MULTIPROC_DIR"], ignore_errors=True)
    os.makedirs(os.environ["PROMETHEUS_MULTIPROC_DIR"], exist_ok=True)

# Load environment variables from .env


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
    