# run_hypercorn.py
import sys
sys.dont_write_bytecode = True
from app.main import app

if __name__ == "__main__":
    app.run(debug=True, port=8000)
print()