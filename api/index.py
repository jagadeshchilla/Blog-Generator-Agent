import sys
import os

# Add project root to Python path - this is critical for Vercel
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base not in sys.path:
    sys.path.insert(0, base)

from mangum import Mangum
from app import app

handler = Mangum(app, lifespan="off")

