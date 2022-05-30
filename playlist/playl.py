import functools
from flask import (
    Blueprint, session, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .auth import login_required
from .db import get_db

bp = Blueprint('playl', __name__)

@bp.route('/')
@login_required
def index():
    db, c = get_db()
    c.execute(
        'select p.id, p.description, p.icon, u.username, p.created_at '
        'from playlisttitle p JOIN user u on p.created_by = u.id ' 
        'where p.created_by = %s order by created_at desc', 
        (g.user['id'],)
    )
    playlists = c.fetchall()

    return render_template('playl/index.html', playlists=playlists)


@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        icon = request.form['icon'] 
        error = None

        if not description:
            error = 'El nombre es requerido'
        if not icon:
            error = 'selecciona una opcion'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'insert into playlisttitle (description, icon, created_by) '
                'values (%s, %s, %s)',
                (description, icon, g.user['id'])
            )
            db.commit()
            return redirect(url_for('playl.index'))
    return render_template('playl/create.html')

def get_playlist(id):
    db, c = get_db()
    c.execute(
        'select p.id, p.description, p.icon, p.created_by, p.created_at, u.username '
        'from playlisttitle p JOIN user u on p.created_by = u.id where p.id = %s',
        (id,)
    )
    playlist = c.fetchone()

    if playlist is None:
        abort(404, "La playlist de id{0} no existe".format(id))
    return playlist

@bp.route('/<int:id>/update', methods = ['GET', 'POST'])
@login_required
def update(id):
    playlist = get_playlist(id)

    if request.method == 'POST':
        description = request.form['description']
        icon = request.form['icon']
        error = None

        if not description:
            error = 'El Nombre es requerido'
        elif not icon:
            error = 'selecciona una opcion'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'update playlisttitle set description = %s, icon = %s'
                ' where id = %s and created_by = %s',
                (description, icon, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('playl.index'))
    return render_template('playl/update.html',playlist=playlist)

@bp.route('/<int:id>/delete', methods = ['POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute(
        'delete from playlisttitle where id = %s and created_by = %s', (id,g.user['id']))
    db.commit()
    return redirect(url_for('playl.index'))
