from bge import logic, types, events, constraints
import random
import os
import aud


scene = logic.getCurrentScene()

class User:
    def __init__(self,name,model_name,position=False):
        self.name = name
        self.model_name = model_name
        self.position = position
        self.speed = 0.1
        self.run = False
        self.jump = False
        self.lock_movement = False
        self.unstopable_animation_tog = False
        self.unstopable_animation_name = None
        self.toggable_keys = [114]
        self.last_send_position  = []
        self.last_send_rotation = []
        self.avatar = self.init_avatar()
        self.main_character = self.avatar
        self.no_response_time = 0
        self.animation = 'stand'

        self.pause_animation = [
            {
                'name':'gymnastic',
                'end': 240
            
            },
            {
                'name':'look',
                'end': 90
            }
        ]

        self.movement = self.get_movement_data()
    
    def init_avatar(self):
        spawner = scene.objects['Spawner']
        avatar = scene.addObject( self.model_name , spawner)

        for chld in avatar.children:
            try:
                chld.text = self.name
            except:
                pass
        avatar['ID'] = self.name
        avatar['jump'] = False
        avatar['fallDown'] = False
        avatar['name'] = 'maniek'

        return avatar

    def get_movement_data(self):

        movement =  {
                        97:{
                            "status":False,
                            "desc":"A",
                            "action":(0,.020,0)
                        },
                        115:{
                            "status":False,
                            "desc":"S",
                            "action":( 0,0,-self.speed )
                        },
                        119:{
                            "status":False,
                            "desc":"W",
                            "action":( 0,0,self.speed )
                        },
                        100:{
                            "status":False,
                            "desc":"D",
                            "action":(0,-.020,0)
                        },
                        32:{
                            "status":False,
                            "desc":"Space"
                        },
                        114:{
                            "status":False,
                            "desc":"R"
                        }
                    }
        return movement
    

    def span_pokemon(self):
        print('SPAAAWN')
        
        pokeball  = scene.objects['pokeball']
        
        pokeball.suspendDynamics()
        files='//sound//pokeball_sound_effects_mp3cut_1.wv'
        files_path = logic.expandPath(files)
        sound = aud.Factory.file(files_path)
        device = aud.device()
        device.volume = 0.01
        device.play(sound)

        pokebalOpenSpawn = scene.addObject('pokeball_spawner', pokeball , 800)
        pokebalOpenSpawn.playAction( 'pokeball_spawner_action', 0, 60 , 0 , speed=2 )

        spawedPok = [x for x in scene.objects if x.name == 'Charizard_sskeleton'] 
        if len(spawedPok ) == 0:

            pokemon = scene.addObject('Charizard_skeleton',pokebalOpenSpawn, 12500)
            pokemon.localOrientation = self.avatar.localOrientation
            pokemon.worldPosition[2] += 3
            pokemon.playAction( 'pokemon_grow', 0 , 60 , 0 )
            
            pokemon['jump'] = False
            pokemon['name'] = 'charizard'
            self.avatar = pokemon

    def move(self):

        no_movement = True
        if self.movement[114]['status']:
            self.run = True
            self.speed = 0.25
            self.movement[119].update( { "action": (0,0,self.speed) } )
        else:
            self.run = False
            self.speed = 0.1
            self.movement[119].update( { "action": (0,0,self.speed) } )
        
        
        for key, value in self.movement.items():
            if value['status'] and self.lock_movement == False:
                
                if key in [97,100]:
                    # rotate
                    self.avatar.applyRotation( value['action'], True )
                if key in [119]:
                    no_movement = False
                    # forward
                    self.avatar.applyMovement( value['action'], True )
                    self.animation = 'move'
                elif key == 32:
                    # jump
                    types.KX_CharacterWrapper.jump(constraints.getCharacter( self.avatar ))
                    self.animation = 'jump'
                    self.avatar.playAction( self.avatar['name']+'_'+self.animation , 0 , 18 , play_mode=0 )
                    self.jump = True
                    self.avatar['jump'] = True
        
        if no_movement and self.avatar['jump'] == False and self.unstopable_animation_tog == False:
            self.animation = 'stand'
    
    def throw_object(self, name):
        right_arm_throw = scene.objects['right_arm_throw']
        throwObject = scene.addObject( name  )

        throwObject.worldPosition = right_arm_throw.worldPosition
        throwObject.localOrientation = self.avatar.localOrientation
        throwObject.worldOrientation = self.avatar.worldOrientation
        
        power = random.randint(2,2)
        throwObject.localLinearVelocity = [0,power,power*10]
        throwObject.localAngularVelocity = [0,2,2]

    def unstopable_animation(self,key):
        if self.jump == False:
            self.animation = self.avatar['name']+'_throw'
            self.unstopable_animation_tog = True
            self.avatar.playAction( self.animation  , 0, 50 , play_mode=0 , priority=1  )
            self.lock_movement = True

    def update_animation(self):

        if self.unstopable_animation_tog == True:
            
            if self.animation == self.avatar['name']+'_throw' and self.avatar.isPlayingAction() and int(self.avatar.getActionFrame() ) == 27:
                self.avatar.setActionFrame(31.0)
                self.throw_object('pokeball')


            elif not self.avatar.isPlayingAction():
                self.lock_movement = False
                self.unstopable_animation_tog = False

        elif self.jump:
            if self.avatar['jump'] == False and self.avatar.isPlayingAction():
                # landing animation
                self.lock_movement = True

            elif self.avatar['jump'] == False and not self.avatar.isPlayingAction():
                # end of jump
                self.lock_movement = False
                self.jump = False
                self.avatar['endJump'] = False
                self.avatar['fallDown'] = False 

        
        elif self.no_response_time >= 1200:
            
            anim = random.choice(self.pause_animation)

            self.avatar.playAction( self.avatar['name']+'_pause_'+anim["name"] , 0, anim['end'] , play_mode=0 )
            # reset no response
            self.no_response_time = 0
        
        elif self.animation == 'move':
            # reset no response
            self.no_response_time = 0

            walkrun = 'run' if self.run else 'walk'

            move_types = {
                "walk":{
                    "name":"walk",
                    "end":30
                },
                "run":{
                    "name":"run",
                    "end":20
                }
            }

            self.avatar.playAction( self.avatar['name']+'_'+move_types[walkrun]['name'] , 0 , move_types[walkrun]['end'] , play_mode=1 , priority=10  )

        elif self.animation == 'stand' and 'pause' not in self.avatar.getActionName() or not self.avatar.isPlayingAction():
            self.no_response_time+=1
            self.avatar.playAction( self.avatar['name']+'_stand' , 0 , 40, play_mode=1 , priority=10 )
