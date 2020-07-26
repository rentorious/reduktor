import functools
import astro_scripts.transformations as tr

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('prelasci', __name__, url_prefix='/prelasci')


@bp.route('/')
def index():
    return render_template('prelasci/index.php')


@bp.route('/transformisi', methods=['GET'])
def transform():
    if request.method == 'GET':
        # coordinate system from witch to convert
        results = tr.convert_system(request.args)
