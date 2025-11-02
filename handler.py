import sys
import os

# Add project root to Python path for Vercel
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mangum import Mangum
from app import app

# Configure Mangum with text_mime_types to handle JSON properly
handler = Mangum(
    app,
    lifespan="off",
    text_mime_types=["application/json", "text/plain"]
)

