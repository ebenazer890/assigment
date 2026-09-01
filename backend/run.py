#!/usr/bin/env python
"""Startup script for backend"""
import sys
import os
from pathlib import Path

# Set up paths - add modus root to sys.path
modus_root = Path(__file__).parent.parent
sys.path.insert(0, str(modus_root))
sys.path.insert(0, str(modus_root / "backend"))

# Change to backend directory
os.chdir(str(modus_root / "backend"))

# Import and run uvicorn
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
