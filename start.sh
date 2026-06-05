#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "========================================="
echo "   Arknights RIIC Calculator - Startup"
echo "========================================="

# ---- Backend Setup & Start ----
echo ""
echo "[1/4] Setting up backend virtual environment..."
cd "$PROJECT_DIR/backend"

if [ ! -d "venv" ]; then
    echo "  -> Creating venv..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "[2/4] Installing backend dependencies..."
pip install -r requirements.txt -q

echo "[3/4] Starting Django backend..."
python manage.py runserver &
BACKEND_PID=$!
echo "  -> Backend PID: $BACKEND_PID"

# ---- Frontend Setup & Start ----
echo ""
echo "[4/4] Starting frontend dev server..."
cd "$PROJECT_DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "  -> Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
echo "  -> Frontend PID: $FRONTEND_PID"

# ---- Info ----
echo ""
echo "========================================="
echo "  Backend:  http://127.0.0.1:8000/"
echo "  Frontend: http://localhost:5173/"
echo "========================================="
echo ""
echo "Press Ctrl+C to stop all servers."

# Trap to kill both processes on exit
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    wait
    echo "All servers stopped."
}
trap cleanup EXIT INT TERM

# Wait for either process to exit
wait
