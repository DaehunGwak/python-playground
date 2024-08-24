from flask import Flask

from search import search_views, search_api_views

app = Flask(__name__)


if __name__ == "__main__":
    app.register_blueprint(search_views.bp)
    app.register_blueprint(search_api_views.bp)
    app.run()
