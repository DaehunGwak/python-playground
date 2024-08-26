from typing import List

from flask import Blueprint, request, jsonify

from web_scrapper.models import JobDescription
from web_scrapper.berlinstartup.services import scrap_berlin_job_descriptions
from web_scrapper.web3.services import scrap_web3_job_descriptions

bp = Blueprint('search_api', __name__, url_prefix='/api')


@bp.route("/search")
def api_search():
    query = request.args.get("query")

    results: List[JobDescription] = []
    results.extend(scrap_berlin_job_descriptions(query=query))
    results.extend(scrap_web3_job_descriptions(tag=query))

    return jsonify({
        "results": results
    })
