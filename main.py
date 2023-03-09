from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import parser2

app = Flask(__name__)
app.config['SQLAlCHEMY_DATABASE_URI']= 'sqlite///base.db'
db.SQLAlchemy(app)

class Article(db.Model):
    id = db.Colum(db.Integer, primery_key=True)
    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/',methods=['get', 'post'])
def index():
    if request.method == "POST":
        url = request.form.get('url')
        return parser2.main2(url)
    else:
        return render_template("index.html")


def red(url):
    return url



if __name__ == '__main__':
    app.run(debug=True)
