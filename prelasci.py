import functools
from astro_scripts import (
    helpers as hlp
)
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('prelasci', __name__, url_prefix='/prelasci')


@bp.route('/')
def index():
    return render_template('prelasci/index.html')

@bp.route("/system_info", methods=['GET'])
def system_info():
    if request.method == 'GET':
        system = request.args["system"]
        result = hlp.get_system_info(system)

        return jsonify(result)


@bp.route('/transformisi', methods=['GET'])
def transform():
    return "haua"

    if request.method == 'GET':
        # coordinate system from witch to convert
        # results = tr.convert_system(request.args)
        pass
