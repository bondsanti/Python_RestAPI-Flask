from flask import request
URL="http://127.0.0.1:5000/weather"
res = request.get(URL)
message = res.json()
print(message)

