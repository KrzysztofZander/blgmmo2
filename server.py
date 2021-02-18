import time
from bge import logic, types, events, constraints
from mathutils import Vector
import threading
import socket
from websocket import create_connection, WebSocket
import json
from user import User
from inputs import get_gamepad
from pynput.keyboard import Key, Controller

keyboard_simulate = Controller()

keyboard = logic.keyboard
gamepads = logic.joysticks

# My Xbox gamepad
# 'Wireless Gamepad'
# 'XInput Controller #2'

xpads = [ x for x in gamepads if x != None and 'XInput' in x.name ]

for p in xpads:

    xpad = xpads[0]

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED

def current_milli_time():
    return round(time.time() *1000 )

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()

class MyWebSocket(WebSocket):
    
    def init_some_value(self):
        self.value = 'test value'
    
    def recv_frame(self):
        frame = super().recv_frame()
        return frame

''' C L I E N T '''
class Client:
    
    def __init__(self, name, password, modelname , host="wss://dvabk2vzn2.execute-api.eu-west-1.amazonaws.com/demo?user="):
        self.ws = create_connection(host+name+"&password="+password,
                        sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),), class_=MyWebSocket)
        self.ws.send( json.dumps( {"action":"getAllPlayers"} ) )
        self.GAME_ON = True

        self.last_mouse_position = 0
        self.mouse_rotation = 0
        self.send_mouse_rotation = False
        self.orient1 = [0,0,0]
        self.orient2 = [0,0,0]
        self.orient0 = [0,0,0]
        
        self.server_response_buffer = []
        self.server_action = []
        self.keys_buffer = []
        
        self.game_pad_keys = {
            "jump":False,
            "run":False,
            "cast":False,
        }
        self.pad_X_axis_last_value = 0
        self.pad_Y_axis_last_value = 0

        self.user = User(name, modelname)
        self.all_users = [self.user]

        self.run()

        for thread in threading.enumerate(): 
            print( thread.name )

    def run(self):
        self.recv_from_ws_t = StoppableThread(target=self.receive_from_ws)
        self.recv_from_ws_t.name  = 'recv_from_ws_t'

        #self.gamepad_action_t = StoppableThread(target=self.gamepad_action)
        #self.gamepad_action_t.name  = 'gamepad_action_t'

        self.recv_from_ws_t.start()
        #self.gamepad_action_t.start()

    def receive_from_ws(self):

        while self.GAME_ON:
            try:
                resp =  json.loads( self.ws.recv() )
                if 'event' in resp:
                    self.server_response_buffer.append( resp )
                elif 'action' in resp:
                    self.server_action.append( resp )
            except Exception as e:
                print(e)

    def process_server_data(self):
        try:
            if current_milli_time() >= self.server_response_buffer[0]['time']:
                resp_data = self.server_response_buffer.pop(0)

                user = [ x for x in self.all_users if x.name == resp_data['data']['user'] ][0]
                key = resp_data['data']['key']

                if resp_data['event'] == 'key_pressed':
                    # Unstopable animation // FIX THIS
                    if key in [113]:
                        user.unstopable_animation( key )
                    
                    user.movement[ key ]['status'] = True

                elif resp_data['event'] == 'key_released':

                    user.movement[ key ]['status'] = False
                
                elif resp_data['event'] == 'rotation':

                    user.avatar.worldOrientation[0] = Vector( resp_data['data']['value'][0] )
                    user.avatar.worldOrientation[1] = Vector( resp_data['data']['value'][1] )
                    user.avatar.worldOrientation[2] = Vector( resp_data['data']['value'][2] )
                
                print( resp_data , current_milli_time() - resp_data['time'] )
        
        except Exception as e:
            pass

    def send_action_to_server(self,act,key,additionalDelay=0 ):

        action =  {
            "time":current_milli_time()+200+additionalDelay,
            "event":act,
            "data":{
                "key":key,
                "user":self.user.name
                }
            }
        self.ws.send( json.dumps(action) )

    def key_kayboard_action(self):
        
        # Send keys with certain delay
        for key in keyboard.events:
            if keyboard.events[key] == JUST_ACTIVATED or keyboard.events[key] == JUST_RELEASED:
                # print(key)
                ''' Leave Game '''
                if key == 130:
                    #kill_player = {"act":"update_pos","user":self.user.name , "data":{"position":"kill"}}
                    #self.ws.send( json.dumps( kill_player ) )
                    time.sleep(0.1)
                    self.GAME_ON = False
                    #self.ws.close()
                    logic.endGame()

                else:
                    act = 'key_pressed' if keyboard.events[key] == JUST_ACTIVATED else 'key_released'
                    self.send_action_to_server(act,key)

    def gamepad_action(self,ROTABLE_SPAWNER):


        try:
            btn = xpad.activeButtons
            axis = xpad.axisValues

            left_right = axis[0]
            walk = axis[1]
            run =  axis[5]
            rotate = round( axis[3], 3)

            if 0.3 > rotate > -0.3:
                rotate = 0
            rotate/=30*-1

            sensiti = 0.5

            if left_right >= sensiti or left_right <= sensiti*-1 or sensiti-.1 > left_right > (sensiti-.1)*-1  :
                ''' Rotate player by gamepad '''

                if sensiti-.1 > left_right > (sensiti-.1)*-1:
                    left_right = 0
                elif left_right >= sensiti:
                    left_right = 100
                elif left_right <= sensiti*-1:
                    left_right = 97
                
                if left_right == 0 and left_right != self.pad_X_axis_last_value:
                    # rel key

                    self.send_action_to_server('key_released', self.pad_X_axis_last_value)
                    self.pad_X_axis_last_value = left_right
                
                elif left_right != self.pad_X_axis_last_value:
                    # press key
                    self.send_action_to_server('key_pressed', left_right )
                    self.pad_X_axis_last_value = left_right

            if walk :
                ''' walk player by gamepad '''
                walk *=-1
                if 0.3 > walk:
                    walk = 0
                else:
                    walk = 119

                if walk == 0 and walk != self.pad_Y_axis_last_value:
                    # rel key

                    self.send_action_to_server('key_released', self.pad_Y_axis_last_value)
                    self.pad_Y_axis_last_value = walk
                
                elif walk != self.pad_Y_axis_last_value:
                    # press key
                    self.send_action_to_server('key_pressed', walk )
                    self.pad_Y_axis_last_value = walk

            actions = [
                {
                    'type':'jump',
                    'key':32,
                    'code':0
                },
                {
                    'type':'run',
                    'key':114,
                    'code':5
                },
                {
                    'type':'cast',
                    'key':113,
                    'code':2
                },
            ]
            
            # rotate
            ROTABLE_SPAWNER.applyRotation( [0,0,rotate] )

            # print(rotate)

            for act in actions:
            
                if self.game_pad_keys[ act['type'] ] and act['code'] not in btn:
                    ''' rel key '''
                    key = act['key']
                    self.send_action_to_server( 'key_released', key )
                    self.game_pad_keys[ act['type'] ] = False
                
                
                elif self.game_pad_keys[ act['type'] ] == False and act['code'] in btn:
                    ''' press key '''
                    key = act['key']
                    self.send_action_to_server( 'key_pressed', key )
                    self.game_pad_keys[ act['type'] ] = True

        except :
            pass


    def mouse_rotation_action(self):

        try:
            if self.orient0 != [0,0,0] and Vector(self.orient0) != self.user.avatar.children['rotation_mock'].worldOrientation[0] :
                
                print('move')

                orient0 = [ round(x,4) for x in self.orient0 ]
                orient1 = [ round(x,4) for x in self.orient1 ]
                orient2 = [ round(x,4) for x in self.orient2 ]

                action =  {
                        "time":current_milli_time()+200,
                        "event":'rotation',
                        "data":{
                            "value":[orient0, orient1 ],
                            "user":self.user.name
                            }
                        }
                self.ws.send( json.dumps(action) )
        except:
            pass
        self.orient0 = list( self.user.avatar.children['rotation_mock'].localOrientation[0] )
        self.orient1 = list( self.user.avatar.children['rotation_mock'].localOrientation[1] )
        self.orient2 = list( self.user.avatar.children['rotation_mock'].localOrientation[2] )
