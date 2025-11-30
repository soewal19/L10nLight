import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add the current directory to the Python path
sys.path.append(os.getcwd())

# Set environment variables
os.environ["APP_ENV"] = "test"
os.environ["APP_SERVER_HOST"] = "0.0.0.0"
os.environ["APP_SERVER_PORT"] = "5000"
os.environ["APP_ALLOWED_ORIGINS"] = '["*"]'
os.environ["APP_GRANIAN_WORKERS"] = "1"
os.environ["APP_DB_URL"] = "sqlite+aiosqlite:///./test.sqlite"
os.environ["APP_ECHO_SQL"] = "True"

logger.info("Starting the application...")

# Import and run the app
try:
    logger.info("Importing app.server...")
    from app.server import app
    logger.info("App imported successfully")
except Exception as e:
    logger.error(f"Error importing app: {e}", exc_info=True)
    raise

if __name__ == "__main__":
    try:
        logger.info("Starting uvicorn server...")
        import uvicorn
        uvicorn.run(
            "app.server:app",
            host="0.0.0.0",
            port=5000,
            reload=True,
            log_level="debug"
        )
    except Exception as e:
        logger.error(f"Error starting server: {e}", exc_info=True)
        raise
