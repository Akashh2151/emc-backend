from flask import Flask
app=Flask(__name__) 
from controller import*


@app.route("/")
def welcome():
    return "hellow Akash"


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    app.run(debug=True)