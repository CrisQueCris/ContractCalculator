from ftplib import error_perm
import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskcontr.db import get_db

bp = Blueprint('contract', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def addcontr():
    if request.method == 'POST':
        commodity = request.form['commodity']
        amount_tonnes = request.form['amount_tonnes']
        amount_euros = request.form['amount_tonnes']
        date_fullfillment = request.form['date_fullfillment']
        db = get_db()
        error= None

        if not commodity:
            error = 'commodity is required'
        elif not amount_tonnes:
            error = 'tonnes are required'
        elif not amount_euros:
            error = 'euros is required'
        elif not date_fullfillment:
            error = 'fullfillment date is required'
        
        if error is None:
            try:
                db.execute(
                    'INSERT INTO contracts (commodity, amount_tonnes, amount_euros, date_fullfillment) VALUES (?, ?, ?, ?)',
                    (commodity, amount_tonnes, amount_euros, date_fullfillment),
                )
                db.commit()
            except db.IntegrityError:
                error = "Couldn't add contract"
            else:
                return redirect(url_for('contract.addcontr'))

        flash(error)

    return render_template('base.html')