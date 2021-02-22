from bge import logic, types, events, constraints
import random
import os
import aud
from pokemon import *
#from pokemon import 
#from pokemon import Mewtwo , Pikachu , Charmeleon , Wartortle , Blastoise , Ivysaur , Venusaur , Oddish

scene = logic.getCurrentScene()

test_Poke = [ Bulbasaur(level=2), 
            Ivysaur(level=2),
            Venusaur(level=2),
            Squirtle(level=2),
            Wartortle(level=2),
            Blastoise(level=2),
            Charmander(level=2),
            Charmeleon(level=2),
            Charizard(level=2),
            Psyduck(level=2),
            Scyther(level=2),
            Jigglypuff(level=2),
            Cubone(level=2),
            Meow(level=2),
            Mewtwo(level=2),
            Pikachu(level=2),

    ]

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
        
        self.pokemon_avatar  = avatar

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
        print('SPAAAWN')
        print('SPAAAWN')
        active_scenes = logic.getSceneList()
        print(active_scenes)
        pokeball  = scene.objects['pokeball']
        
        pokeball.suspendDynamics()

        files='//sound//pokeball_sound_effects_mp3cut_1.wv'
        files_path = logic.expandPath(files)
        sound = aud.Factory.file(files_path)
        device = aud.device()
        pokebal_sound = device.play(sound)
        pokebal_sound.volume = 0.2

        pokebalOpenSpawn = scene.addObject('pokeball_spawner', pokeball , 200)
        pokebalOpenSpawn.playAction( 'pokeball_spawner_action', 0, 60 , 0 , speed=2 )

        spawedPok = [x for x in scene.objects if x.name == 'Scythesr_skeleton']

        test_spawned_pokemon = random.choice( test_Poke ) 

        if len(spawedPok ) == 0: 

            pokemon = scene.addObject( test_spawned_pokemon.model ,pokebalOpenSpawn)
            pokemon.localOrientation = self.avatar.localOrientation
            pokemon.worldPosition[2] += 3
            pokemon.playAction( 'pokemon_grow', 0 , 60 , 0 )
            
            pokemon['jump'] = False
            pokemon['name'] = test_spawned_pokemon.name
            self.pokemon_avatar = test_spawned_pokemon
            self.avatar = pokemon

            files = self.pokemon_avatar.get_sound()
            files_path = logic.expandPath(files)
            sound = aud.Factory.file(files_path)
            device2 = aud.device()
            device2.volume = 0.3
            device2.play(sound)

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
            self.animation = 'maniek_throw'
            self.unstopable_animation_tog = True
            self.avatar.playAction( self.animation  , 0, 50 , play_mode=0 , priority=1  )
            self.lock_movement = True

    def update_animation(self):


        try:
            if self.unstopable_animation_tog == True:
                
                if self.animation == 'maniek_throw' and self.avatar.isPlayingAction() and int(self.avatar.getActionFrame() ) == 27:
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
                        "end": self.pokemon_avatar.anim_walk[1]
                    },
                    "run":{
                        "name":"run",
                        "end":self.pokemon_avatar.anim_run[1]
                    }
                }

                self.avatar.playAction( self.avatar['name']+'_'+move_types[walkrun]['name'] , 0 , move_types[walkrun]['end'] , play_mode=1 , priority=10  )

            elif self.animation == 'stand' and 'pause' not in self.avatar.getActionName() or not self.avatar.isPlayingAction():
                
                self.no_response_time+=1
                self.avatar.playAction( self.avatar['name']+'_stand' , 0 , self.pokemon_avatar.anim_stand[1], play_mode=1 , priority=10 )
        except :
            pass