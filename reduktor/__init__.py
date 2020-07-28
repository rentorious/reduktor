import os
from flask import Flask, redirect, url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABSE=os.path.join(app.instance_path, 'prakticna-projekat.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exist, when not testing
        app.config.from_pyfile('config.py', silent=True)
    # else:
        # load the test config if passed in
        # app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import prelasci
    app.register_blueprint(prelasci.bp)


    @app.route('/')
    def hello():
        return redirect(url_for('prelasci.index'))

    print("HELLO THERE")

    return app
