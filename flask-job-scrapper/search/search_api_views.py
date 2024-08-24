from typing import List

from flask import Blueprint, request, jsonify

from web_scrapper.models import JobDescription
from web_scrapper.services import scrap_job_descriptions

bp = Blueprint('search_api', __name__, url_prefix='/api')


@bp.route("/search")
def api_search():
    query = request.args.get("query")
    page = request.args.get("page")
    if page is None:
        page = 1

    results: List[JobDescription] = []

    for jobs in scrap_job_descriptions(query=query):
        results.extend(jobs)

    return jsonify({
        "results": results
    })
