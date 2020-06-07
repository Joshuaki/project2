import os

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

class Channel:
    message_limit = 100
    def __init__(self, creator, channelName, description):
        self.creator = creator
        self.channelName = channelName
        self.description = description
        self.messages = []
    def add_message(self, user, time_stamp, message):
        if len(self.messages) > 0:
            message_id = self.messages[-1]["id"] + 1
        else:
            message_id = 0
        self.messages.append({"id": message_id,  "user": user, "time stamp": time_stamp, "message": message})
        if len(self.messages) > self.message_limit:
            self.messages.pop(0)
    def delete_message(self, message_id, user, time_stamp, message):
        message_index = self.messages.index({"id": message_id,  "user": user, "time stamp": time_stamp, "message": message})
        self.messages.pop(message_index)

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
    
'''
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
 '''   

#channels = flack.channelObj

#for channel_name, channel_object in channels.items():
#@app.route('/{}'.format(channel_name), methods=['GET'])

@app.route('/channel/<channel_name>', methods=['GET'])
def channel_content(channel_name):
    channels = flack.channelObj
    channel = channels[channel_name]
    print({'channel creator': channel.creator, 'channel name': channel.channelName, 
                    'channel description': channel.description, 'channel messages': channel.messages})
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
    message_data = messages[-1]     
    message = message_data["message"]
    message_id = message_data["id"]
    message_dp = message_data["user"]
    message_ts = message_data["time stamp"]


    emit("announce message", {"id": message_id, "message text": message, "display name": message_dp, "time stamp": message_ts}, broadcast=True)

'''socket.emit('delete message', {'id': id, 
                                'time stamp': time_stamp, 
                                'display name': display_name, 
                                'channel name': channel_name, 
                                'message text': message_text})'''

@socketio.on('delete message')
def delete_message(data):
    message_id = data['id']
    time_stamp = data['time stamp']
    display_name = data['display name']
    channel_name = data['channel name']
    message_text = data['message text']

    #channel object
    channels = flack.channelObj
    channel = channels[channel_name]

    channel.delete_message(message_id=message_id, user=display_name, time_stamp=time_stamp, message=message_text)
  

if __name__ == "__main__":
    socketio.run(app)
