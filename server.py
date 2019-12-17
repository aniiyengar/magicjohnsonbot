
from nba import NBAScore
from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    s = ''
    try:
        s = NBAScore().get_status()
    except:
        s = 'No NBA games yet!'

    return '<p style="font-size: 24px;">' + s + '</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
