from flask import Flask 

app = Flask (__name__) 

@app.route("/")
def home():
    return("<H1>The Revival Has Begun</H1>")

if __name__ == "__main__":
    app.run(debug=True)