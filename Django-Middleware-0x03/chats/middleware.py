# # chats/middleware.py
# import logging
# from datetime import datetime

# # Configure the logger to write to requests.log
# logger = logging.getLogger("request_logger")
# handler = logging.FileHandler("requests.log")
# formatter = logging.Formatter("%(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)


# class RequestLoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         user = request.user if request.user.is_authenticated else "Anonymous"
#         log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
#         logger.info(log_message)

#         response = self.get_response(request)
#         return response

# # chats/middleware.py
# import logging
# from datetime import datetime
# import os

# log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "requests.log")

# logger = logging.getLogger("request_logger")
# if not logger.handlers:
#     handler = logging.FileHandler(log_file_path)
#     formatter = logging.Formatter("%(message)s")
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     logger.setLevel(logging.INFO)


# class RequestLoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         user = request.user if request.user.is_authenticated else "Anonymous"
#         log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
#         print(f"Logging request: {log_message}")  # 🐛 Debug: show in terminal
#         logger.info(log_message)

#         return self.get_response(request)

import os
import logging
from datetime import datetime

# Log file path (inside your Django project root directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "requests.log")

# Ensure logger is configured only once
logger = logging.getLogger("request_logger")
if not logger.hasHandlers():
    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = (
            request.user
            if hasattr(request, "user") and request.user.is_authenticated
            else "Anonymous"
        )
        message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(message)
        return self.get_response(request)
