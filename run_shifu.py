import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from shifu.app import app

if __name__ == '__main__':
    print("\n>> Shifu Backend running on port 5001!")
    print("Endpoints:")
    print("   POST   http://localhost:5001/api/shifu        -> Submit form")
    print("   GET    http://localhost:5001/api/shifu        -> Get all submissions")
    print("   GET    http://localhost:5001/api/shifu/<id>   -> Get one by ID")
    print("   PUT    http://localhost:5001/api/shifu/<id>   -> Update by ID")
    print("   DELETE http://localhost:5001/api/shifu/<id>   -> Delete by ID\n")
    app.run(host='0.0.0.0', port=5001, debug=True)
