#!/usr/bin/env python
from app import app
#app.run(debug=True)
#app.run('0.0.0.0', port=5000)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 80)
