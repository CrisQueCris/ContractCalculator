from ftplib import error_perm
import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskcontr import get_db

bp = Blueprint('contract', __name__, url_prefix='/contract')

@bp.route('/addcontr', methods=('GET', 'POST'))
def addcontr():
    if addcontr.method == 'POST':
        commodity = addcontr.form['commodity']
        amount_tonnes = addcontr.form['amount_tonnes']
        amount_euros = addcontr.form['amount_tonnes']
        date_fullfillment = addcontr.form['date_fullfillment']
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
                return redirect(url_for('index'))

        flash(error)

    return render_template('contract/addcontr.html')