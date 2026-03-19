#!/bin/bash
set -e

echo "=== Starting Build Script ==="
echo "Current directory: $(pwd)"
echo "Contents: $(ls -la)"

cd backend
echo "=== Changed to backend directory ==="
echo "Current directory: $(pwd)"

echo "=== Upgrading pip ==="
pip install --upgrade pip

echo "=== Installing requirements ==="
pip install -r requirements.txt

echo "=== Verifying installations ==="
pip list | grep -E "(uvicorn|fastapi|pydantic)"

echo "=== Build Complete ==="
