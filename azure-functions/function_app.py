import os
import sys

# Reuse the existing Flask app object from frontend/src/app.py instead of
# duplicating route/business logic for the Functions runtime.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "frontend", "src"))

import azure.functions as func
from app import app as flask_app  # noqa: E402  (the Flask() instance in frontend/src/app.py)

func_app = func.FunctionApp()


@func_app.route(route="{*route}", auth_level=func.AuthLevel.ANONYMOUS)
def frontend(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.WsgiMiddleware(flask_app.wsgi_app).handle(req, context)
