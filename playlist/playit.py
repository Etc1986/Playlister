from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session 
)
from werkzeug.exceptions import abort
from playlist.auth import login_required
from playlist.db import get_db


bp = Blueprint('playit', __name__)

@bp.route('/playit')
@login_required
def playit():
    db, c = get_db()
    c.execute(
        'select i.id, i.created_for, i.title, i.artist, '
        'i.year, i.genre, p.description from playlistcontent i '
        'JOIN playlisttitle p on i.created_for = p.id '
        'where i.created_for = %s order by id ', 
        ( g.playlisttitle['id'],)
    )
    playlistits = c.fetchall()

    return render_template('playl/playit.html', playlistits=playlistits,)

@bp.before_request
def load_logged_in_pl():
        db, c = get_db()
        c.execute(
            'select p.id from playlisttitle p join user u '
            'where u.id = created_by and created_by = %s',(g.user['id'],)
        )
        g.playlisttitle = c.fetchone()


@bp.route('/createItems', methods = ['GET', 'POST'])
@login_required
def createItems():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        year = request.form['year']
        genre = request.form['genre'] 
        error = None

               
        if not title:
            error = 'El titulo es requerido'
        if not artist:
            error = 'El artista es requerido'
        if not year:
            error = 'El año es requerido'
        if not genre:
            error = 'El genero es requerido'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(

                'insert into playlistcontent (title, artist, year, genre, created_for) '
                'values (%s, %s, %s, %s, %s)',
                (title, artist, year, genre, g.playlisttitle['id'] )
            )
            db.commit()
            return redirect(url_for('playit.playit'))
    return render_template('playl/createItems.html')


def get_playlistI(id):
    db, c = get_db()
    c.execute(
        'select i.id, i.title, i.artist, i.year, i.genre, '
        'i.created_for, p.description '
        'from playlistcontent i JOIN playlisttitle p '
        'on i.created_for = p.id where i.id = %s',
        (id,)
    )
    playlistI = c.fetchone()

    if playlistI is None:
        abort(404, "La canción de id {0} no existe".format(id))
    return playlistI

@bp.route('/<int:id>/updateItems', methods = ['GET', 'POST'])
@login_required
def updateItems(id):
    playlistI = get_playlistI(id)

    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        year = request.form['year']
        genre = request.form['genre'] 
        error = None

        if not title:
            error = 'El Nombre es requerido'
        if not artist:
            error = 'El artista es requerido'
        if not year:
            error = 'El año es requerido'
        if not genre:
            error = 'El genero es requerido'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'update playlistcontent set title = %s, artist = %s, '
                'year = %s, genre = %s'
                ' where id = %s',
                (title, artist, year, genre, id)
            )
            db.commit()
            return redirect(url_for('playit.playit'))
    return render_template('playl/updateItems.html',playlistI=playlistI)

@bp.route('/<int:id>/deleteI', methods = ['POST'])
@login_required
def deleteI(id):
    db, c = get_db()
    c.execute(
        'delete from playlistcontent where id = %s and created_for = %s', 
        (id, g.playlisttitle['id'])
    )
    db.commit()
    return redirect(url_for('playit.playit'))
