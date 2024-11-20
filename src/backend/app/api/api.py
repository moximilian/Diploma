"""
Entry point for all endpoints
"""

import os
import importlib
from fastapi import APIRouter
from env_constants import BASE_URL

app_router = APIRouter()


def include_routers(app_router: APIRouter):
    endpoints_path = os.path.join(os.path.dirname(__file__), 'endpoints')
    for filename in os.listdir(endpoints_path):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            try:
                module = importlib.import_module(
                    f'api.endpoints.{module_name}')
                if hasattr(module, 'router'):
                    app_router.include_router(
                        module.router, prefix=f'/{BASE_URL}', tags=[module_name])
                    print(f'{module} router is added')
            except Exception as e:
                print(f'Failed to include router from {filename}: {e}')


include_routers(app_router)
