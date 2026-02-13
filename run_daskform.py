import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from daskform.app import app

if __name__ == '__main__':
    print("\n>> DaskForm Backend running on port 5000!")
    print("Endpoints:")
    print("   POST   http://localhost:5000/api/daskform        -> Submit form")
    print("   GET    http://localhost:5000/api/daskform        -> Get all submissions")
    print("   GET    http://localhost:5000/api/daskform/<id>   -> Get one by ID")
    print("   PUT    http://localhost:5000/api/daskform/<id>   -> Update by ID")
    print("   DELETE http://localhost:5000/api/daskform/<id>   -> Delete by ID\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
