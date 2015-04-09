from flask import Flask

from .loader import CustomPackageLoader

app = Flask(__name__)


loader = CustomPackageLoader(template_modules=['client_custom', 'shared',
                                               'base'])
base_only = CustomPackageLoader(template_modules=['base'])


@app.route('/')
def index():
    return loader.load('index')().render()


@app.route('/base_only')
def base():
    return base_only.load('index')().render()


def main():
    app.run(debug=True)
