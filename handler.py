import sys
import os

# Add project root to Python path for Vercel
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from mangum import Mangum
    from app import app
    
    # Verify routes are registered
    routes = [route.path for route in app.routes]
    print(f"Registered routes: {routes}")
    
    # Configure Mangum - use api_gateway_base_path for Vercel
    handler = Mangum(
        app,
        lifespan="off",
        api_gateway_base_path="/"
    )
except Exception as e:
    import traceback
    error = f"Handler initialization error: {str(e)}\n{traceback.format_exc()}"
    print(error)
    
    def handler(event, context):
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': error
        }

