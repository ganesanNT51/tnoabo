from core import app
# from core import app, socketio
if __name__ == '__main__':
    # socketio.run(app,host='0.0.0.0',port=80,debug=True)
    app.run(host='0.0.0.0',port=80,debug=True,threaded=True)


