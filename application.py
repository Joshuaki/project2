import os

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

class Channel:
    def __init__(self, creator, channelName, description):
        self.creator = creator
        self.channelName = channelName
        self.description = description
        self.messages = []
    def add_message(self, user, time_stamp, message):
        self.messages.append({"user": user, "time stamp": time_stamp, "message": message})

class Channels:
    channels = []
    channelObj = {}
    def add_channel(self, creator, channelName, description):
        temp = Channel(creator, channelName, description)
        self.channels.append(temp)
        self.channelObj[temp.channelName] = temp
        #self.channels[channelName] = [temp.creator, temp.description]
    def channel_data(self):
        channelData = {}
        for channel in self.channels:
            channelData[channel.channelName] = {'creator': channel.creator, 'description': channel.description, 'messages': channel.messages}
        return channelData
    

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

flack = Channels() 


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/channelList")
def channel_list():
    return jsonify(flack.channel_data())

@app.route('/newChannel', methods=['POST'])
def new_channel():

    
    channelName = request.form.get('channelName')
    if channelName in flack.channel_data():
        return jsonify({channelName: {'description': False}})

    #queries for channel information
    creator = request.form.get('creator')
    channelDescription = request.form.get('channelDescription')
    flack.add_channel(creator, channelName, channelDescription)

    return jsonify(flack.channel_data())
    #return jsonify({'channelName': channelName, 'creator': creator, 'channelDescription': channelDescription})
    

@app.route('/channel', methods=['POST'])
def channel():

    channel_name = request.form.get('channel name')

    #Using channel name, get channel object
    channels = flack.channelObj
    channel = channels[channel_name]

    """self.creator = creator
        self.channelName = channelName
        self.description = description
        self.messages = []"""

    
    return jsonify({'channel creator': channel.creator, 'channel name': channel.channelName, 
                    'channel description': channel.description, 'channel messages': channel.messages})
    


@socketio.on('send message')
def send_message(data):

    #{'time stamp': time_stamp, 'display name': display_name, 
    # 'channel name': channel_name, 'message text': message_text}

    #message data for channel message
    time_stamp = data['time stamp']
    display_name = data['display name']
    channel_name = data['channel name']
    message_text = data['message text']

    

    #add message to channel object
    channels = flack.channelObj
    channel = channels[channel_name]
    channel.add_message(user=display_name, time_stamp=time_stamp, message=message_text)
    
    
    messages = channel.messages
    last_message = messages[-1]     
    new_message = last_message["message"]
    new_message_dp = last_message["user"]
    new_message_ts = last_message["time stamp"]


    emit("announce message", {"message text": new_message, "display name": new_message_dp, "time stamp": new_message_ts}, broadcast=True)



if __name__ == "__main__":
    socketio.run(app)
