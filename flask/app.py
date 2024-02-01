from flask import Flask

app = Flask(__name__)

@app.route('/') # Whenever we go to this url '/' 
def hello(): # we run this function
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True) # Run the app in debug mode