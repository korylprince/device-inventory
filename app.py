from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
app.config['BOOTSTRAP_FONTAWESOME'] = True
app.config['BOOTSTRAP_USE_CDN'] = True
Bootstrap(app)
CsrfProtect(app)

assets = Environment(app)

js = Bundle('js/main.js',
            filters='coffeescript,jsmin', output='min/app.js')
assets.register('js_all', js)

css = Bundle('css/main.css',
            filters='less,cssmin', output='min/screen.css')
assets.register('css_all', css)

@app.route("/")
def hello():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)
