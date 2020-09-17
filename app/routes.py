from flask import render_template
from app import app
from app import scraper

@app.route('/')
@app.route('/index')
def index():
    scraper.scrape()
    return render_template('index.html', title='Home')

