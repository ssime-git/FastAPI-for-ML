import logging
import os

# Create logs directory if it doesn't exist
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging
log_file = os.path.join(log_directory, 'project.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Create a logger instance
custom_logger = logging.getLogger('project_logger')

# Example usage within this module
if __name__ == "__main__":
    custom_logger.debug("This is a debug message")
    custom_logger.info("This is an info message")
    custom_logger.warning("This is a warning message")
    custom_logger.error("This is an error message")
    custom_logger.critical("This is a critical message")