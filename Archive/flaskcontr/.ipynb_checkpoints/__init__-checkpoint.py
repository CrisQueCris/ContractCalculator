import os
from flask import Flask

def create_app(test_config=None):
    #app creation an configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskcontr.sqlite'),

    )

    if test_config is None:
        #loads instance config, if exists when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    #ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import db
    db.init_app(app)

    from . import addcontr
    app.register_blueprint(addcontr.bp)


    from . import futureprice
    futureprice.plot_wheatprice()

    return app
