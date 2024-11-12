"""
Entry point for all endpoints
"""

import os
import importlib
from fastapi import APIRouter, Depends

from ..database import get_db
from .endpoints.items import router as items_router


app_router = APIRouter()
db = Depends(get_db)

def include_routers(app_router: APIRouter):
    endpoints_path = os.path.join(os.path.dirname(__file__), 'endpoints')
    for filename in os.listdir(endpoints_path):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3] 
            try:
                module = importlib.import_module(f'api.endpoints.{module_name}')
                if hasattr(module, 'router'):
                    app_router.include_router(module.router, prefix=f'/{module_name}', tags=[module_name])
            except Exception as e:
                print(f'Failed to include router from {filename}: {e}')

include_routers(app_router)


