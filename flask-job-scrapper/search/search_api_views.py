from typing import List

from flask import Blueprint, request, jsonify

from web_scrapper.models import JobDescription
from web_scrapper.berlinstartup.services import scrap_berlin_job_descriptions
from web_scrapper.web3.service import scrap_web3_job_descriptions

bp = Blueprint('search_api', __name__, url_prefix='/api')


@bp.route("/search")
def api_search():
    query = request.args.get("query")
    page = request.args.get("page") # TODO: Pagination 을 가능하게
    if page is None:
        page = 1

    results: List[JobDescription] = []

    for jobs in scrap_berlin_job_descriptions(query=query):
        results.extend(jobs)
    for jobs in scrap_web3_job_descriptions(tag=query):
        results.extend(jobs)

    return jsonify({
        "results": results
    })
