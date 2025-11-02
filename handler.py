import sys
import os

# Add project root to Python path for Vercel
sys.path.insert(0, os.path.dirname(__file__))

from mangum import Mangum
from app import app

handler = Mangum(app, lifespan="off")

