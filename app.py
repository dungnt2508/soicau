from app import create_app, socketio

if __name__ == '__main__':
    app = create_app()
    # socketio.run(app,debug=True)
    # socketio.run(app=app,debug=True,host='0.0.0.0', port=9007)
    app.run(host='0.0.0.0', port=9007)