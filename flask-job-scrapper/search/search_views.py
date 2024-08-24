from flask import Blueprint, render_template, request

bp = Blueprint('search', __name__, url_prefix='/')


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route("/search")
def search():
    query = request.args.get("query")
    page = request.args.get("page")
    if page is None:
        page = 1

    return render_template('results.html', query=query)
