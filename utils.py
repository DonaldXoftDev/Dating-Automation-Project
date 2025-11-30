import os
import logging
import datetime
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("YOUR_USERNAME")
password = os.getenv("YOUR_PASSWORD")

LOGS_DIR = "logs"
def setup_logger(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the full file path
    log_filename = datetime.datetime.now().strftime("automation_%Y%m%d_%H%M%S.log")
    full_path = os.path.join(directory, log_filename)

    logging.basicConfig(
        # Save messages to the defined file
        filename=full_path,
        # ... (Keep existing file setup and format) ...
        level=logging.INFO,  # Set your primary app level to INFO (or DEBUG if you need detail)
        # Define the format of the log message
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    )

    #  Silence the Noise (Crucial Step!)
    # Set the log level of Selenium's low-level communication to WARNING or higher
    logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)

    # Set the log level of the underlying HTTP connection pool to WARNING
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

    #  Return your application logger
    return logging.getLogger('DatingAutomationLogger')  # Use your application's logger name

