#!/usr/bin/env python3
"""
Startup script for Quantum Portfolio Optimizer Backend
"""
import uvicorn
import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("data/uploads", exist_ok=True)
    
    print("🚀 Starting Quantum Portfolio Optimizer Backend...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔬 Interactive API: http://localhost:8000/redoc")
    print("🌐 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )