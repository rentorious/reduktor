import functools
from .astro_scripts import (
    helpers as hlp
)
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('prelasci', __name__, url_prefix='/prelasci')


@bp.route('/')
def index():
    return render_template('prelasci/index.html')


@bp.route("/system_info", methods=['POST'])
def system_info():
    if request.method == 'POST':
        # system = request.args["system"]
        result = hlp.get_system_info("Horizontski")

        return jsonify(result), 200


@bp.route("/all_systems_info", methods=['POST'])
def all_systems_info():
    if request.method == 'POST':
        result = hlp.get_all_systems_info()

        return jsonify(result), 200


@bp.route('/transformisi', methods=['POST'])
def transform():

    if request.method == 'POST':
        result = hlp.transform_system(request.json)

        return jsonify(result), 200
