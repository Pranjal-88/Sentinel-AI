from flask import Flask, session, abort, redirect, request, render_template, flash, jsonify
from flask_socketio import SocketIO, emit
import eventlet
import json

app = Flask(__name__)
app.secret_key = "bablucopter"
socketio = SocketIO(app)

@app.route("/", methods=['GET', 'POST'])
def cctv_map():
    if request.method == 'POST':
        dataGet = request.get_json(force=True)
        # data = {
        #     'camera':{
        #         'location_id':' ',
        #         'ip':'192.168.50.26',
        #         'activity_detected':'warning message'
        #     },
        # }
        socketio.emit('listener', {
            'camera':{
                'location_id':dataGet['camera']['location_id'],
                'ip':dataGet['camera']['ip'],
                'activity_detected':dataGet['camera']['activity_detected']
            },
        }, namespace='/listener')
        
        return jsonify({})
    else:
        return render_template('index.html', session=session)


@socketio.on('listener', namespace='/listener')
def listener():
    pass

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app, log_output=True, debug=True)
