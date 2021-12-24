from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from random import choice
 

class GameConsumer(WebsocketConsumer):
    possibilities = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ] 
    state = {
        'turn': None,
        'participants': []
    }  
    def connect(self):
        self.scope["session"]["username"] = self.scope["url_route"]['kwargs']['username']
        self.room_name = self.scope['url_route']['kwargs']['code']
        self.room_group_name = f'game_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
 

        username = self.scope['url_route']['kwargs']['username']
        self.accept()
        if username in self.state['participants']:
            self.send(json.dumps({"type": "already_joined"}))
            return
        
        if(len(self.state['participants']) == 2):
            print(self.state["participants"])
            self.send(json.dumps({"type": "room_full"}))
            return
        
        if(username not in self.state["participants"]):
            self.state["participants"].append(username)

            
        if(len(self.state["participants"]) < 2):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "start",
                    "payload": {'start': False, "username":  self.scope["session"]["username"]}
                }
            )
            
        elif len(self.state["participants"]) == 2:
            if(self.state['turn'] is None):
                self.state['turn']  = choice(self.state['participants'])
            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "start",
                    "payload": {'start': True, 'turn': self.state['turn'], "username":  self.scope["session"]["username"] }
                }
            ) 
            
         
    def receive(self, text_data=None, bytes_data=None):
        name = [p for p in (self.state['participants']) ]
        name.remove(self.state["turn"])
        self.state["turn"] = name[0]
        
        print(json.loads(text_data))        
        data = json.loads(text_data) 
        
        if(data["type"] == 'current_state'):
            for possibility in self.possibilities: 
                win = False
                i = 0
                for index in possibility:
                    if(i == 3):
                        break
                    if(index in data["currentState"]):
                        win = True
                        i += 1
                    else:
                        win = False
                        break
                if(win): 
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name, {
                            "type": "win",
                            "payload": {'winner': data['username']}
                        }
                    )
                    return
                if(len(data["currentState"]) == 5):
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name, {
                            "type": "draw", 
                        }
                    )
                    return
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "changeTurn",
                    "payload": {'turn': self.state["turn"], 'state': data["currentState"], "username": data['username']}
                }
            )
        
            
        if(data["type"] == 'restart'):
            self.state['turn']  = choice(self.state['participants'])
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "restart",
                    "payload": {'turn': self.state['turn'] }
                }
            )
        
    
    def disconnect(self, code):
        self.state['participants'].remove(self.scope["session"]["username"])
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "end", 
            }
        )
            
    def start(self, event):
        self.send(json.dumps(event))

    def win(self, event):
        self.send(json.dumps(event))

    def changeTurn(self, event):
        self.send(json.dumps(event))

    def restart(self, event):
        self.send(json.dumps(event))

    def end(self, event):
        self.send(json.dumps(event))
 
 

    def draw(self, event):
        self.send(json.dumps(event))
 
 