from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify,session
from core.model.Comments import Comments
from core.model.User import UserModel 
import datetime
from datetime import timedelta,date,datetime,time
from random import randint
import json,utils


app = Blueprint('comments', __name__)

#---------------Author: Nandhini -------------------------#
@app.route('/comment_index', methods = ["GET","POST"])
def comment_index():
    c = Comments()
    getcomments = c.get_comments()
    # print('getcomments')
    # print(getcomments)
    return render_template('backoffice/comment_index.html',getcomments=getcomments)

@app.route('/comment_reject/<comment_id>', methods = ["GET","POST"])
def comment_reject(comment_id):
    c = Comments()
    reject_comment = c.rejectcomment(comment_id)
    checked = request.form["checked"]
    # print('checked')
    # print(checked)
    data = {
            'is_reject' : checked ,
            'updated_at': datetime.now(),
        }
    print("from ajax data")    
    print(data)        
    save_is_reject = c.saveisreject(comment_id,data)
    
    return jsonify({'data':data })

