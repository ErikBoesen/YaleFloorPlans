from flask import render_template, request, jsonify, g
from flask_cas import login_required
from app import app, db, cas
from app.models import User

import datetime
import time
import yalies

yalies_api = yalies.API(app.config['YALIES_API_KEY'])

@app.before_request
def store_user():
    if request.method != 'OPTIONS':
        if cas.username:
            g.user = User.query.get(cas.username)
            timestamp = int(time.time())
            if not g.user:
                person = yalies_api.person(filters={
                    'netid': cas.username,
                    'school_code': 'YC',
                })
                if not person:
                    abort(403)
                g.user = User(username=cas.username,
                              college_code=person.college_code,
                              registered_at=timestamp)
                db.session.add(g.user)
            g.user.last_seen = timestamp
            db.session.commit()
            print('NetID: ' + cas.username)


@app.route('/')
def index():
    if not cas.username:
        return render_template('splash.html')
    options = yalies_api.filters()
    return render_template('index.html', options=options, filters=filters)
