from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify,session
from core.model.Poster import Poster
from core.model.User import UserModel 
import datetime
from datetime import timedelta,date,datetime,time
from random import randint
import json,utils


app = Blueprint('poster', __name__)

#---------------Author: Nandhini -------------------------#

#-----------Poster--------------#
@app.route('/poster', methods = ["GET","POST"])
def get_poster():
    u = UserModel()
    user = u.Auth()
    if user:
        p = Poster()
        results = p.getposter() 
        # return "test"
        return render_template('poster/poster.html',results=results)
    else :
        # print('No session login')
        return redirect (url_for('user.Login'))

@app.route('/posterarea/<p_date>', methods = ["GET","POST"])
def poster_area(p_date):
    u = UserModel()
    user = u.Auth()
    if user:
        # p_date = p_date.strftime("%d/%m/%y")
        p = Poster()
        results = p.posterarea(p_date) 
        date=results[0].get('date')
        return render_template('poster/posterarea.html',results=results,date=date)
    else :
        # print('No session login')
        return redirect (url_for('user.Login'))

@app.route('/getppt/<poster_id>', methods = ["GET","POST"])
def get_ppt(poster_id):
    u = UserModel()
    user = u.Auth()
    if user:
        p = Poster()
        results = p.get_author_ppt(poster_id) 
        # print('author poster area')
        # print(results)
        # return "test"
        return render_template('poster/author_poster.html',p=results)
    else :
        print('No session login')
        return redirect (url_for('user.Login'))


    