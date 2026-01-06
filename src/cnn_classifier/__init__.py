import os
import sys
import logging

log_format = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"

# Ensure logs directory is created relative to current working directory
log_dir = os.path.join(os.getcwd(), "logs")
log_file = "running_logs.log"
os.makedirs(log_dir, exist_ok=True)
file_path = os.path.join(log_dir, log_file)

# Handlers: console + file (explicitly passed to basicConfig)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
file_handler = logging.FileHandler(file_path, mode="a", encoding="utf-8")
file_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[stream_handler, file_handler]
)

logger = logging.getLogger(__name__)

