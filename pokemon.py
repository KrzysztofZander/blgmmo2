from pathlib import Path
import os

class Pokemon():

    def __init__(self, *args , **kwargs):
        
        self.level = kwargs.get('level')

    def get_sound(self):
        path = 'E:\\blender games\\original-cries\\'
        for root, dirs, files in os.walk( path ) :
            for file_name in files:
                if self.name in file_name.lower():
                    return path+file_name


class Bulbasaur(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Bulbasaur, self).__init__(*args, **kwargs)

        self.type = ['grass']
        self.model = 'Bulbasaur_skeleton'
        self.name = 'bulbasaur'

        # ANIMATION DATA
        self.anim_stand = [0,42]
        self.anim_walk = [0,29]
        self.anim_run = [0,10]

class Ivysaur(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Ivysaur, self).__init__(*args, **kwargs)

        self.type = ['grass']
        self.model = 'Ivysaur_skeleton'
        self.name = 'ivysaur'

        # ANIMATION DATA
        self.anim_stand = [0,49]
        self.anim_walk = [0,39]
        self.anim_run = [0,14]

class Venusaur(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Venusaur, self).__init__(*args, **kwargs)

        self.type = ['grass']
        self.model = 'Venusaur_skeleton'
        self.name = 'venusaur'

        # ANIMATION DATA
        self.anim_stand = [0,59]
        self.anim_walk = [0,39]
        self.anim_run = [0,17]

class Squirtle(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Squirtle, self).__init__(*args, **kwargs)

        self.type = ['water']
        self.model = 'Squirtle_skeleton'
        self.name = 'squirtle'

        # ANIMATION DATA
        self.anim_stand = [0,29]
        self.anim_walk = [0,23]
        self.anim_run = [0,19]

class Wartortle(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Wartortle, self).__init__(*args, **kwargs)

        self.type = ['water']
        self.model = 'Wartortle_skeleton'
        self.name = 'wartortle'

        # ANIMATION DATA
        self.anim_stand = [0,31]
        self.anim_walk = [0,29]
        self.anim_run = [0,19]

class Blastoise(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Blastoise, self).__init__(*args, **kwargs)

        self.type = ['water']
        self.model = 'Blastoise_skeleton'
        self.name = 'blastoise'

        # ANIMATION DATA
        self.anim_stand = [0,79]
        self.anim_walk = [0,39]
        self.anim_run = [0,24]

class Charmander(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Charmander, self).__init__(*args, **kwargs)

        self.type = ['fire']
        self.model = 'Charmander_skeleton'
        self.name = 'charmander'

        # ANIMATION DATA
        self.anim_stand = [0,34]
        self.anim_walk = [0,29]
        self.anim_run = [0,19]

class Charmeleon(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Charmeleon, self).__init__(*args, **kwargs)

        self.type = ['fire']
        self.model = 'Charmeleon_skeleton'
        self.name = 'charmeleon'

        # ANIMATION DATA
        self.anim_stand = [0,59]
        self.anim_walk = [0,29]
        self.anim_run = [0,19]

class Charizard(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Charizard, self).__init__(*args, **kwargs)

        self.type = ['fire']
        self.model = 'Charizard_skeleton'
        self.name = 'charizard'

        # ANIMATION DATA
        self.anim_stand = [0,71]
        self.anim_walk = [0,47]
        self.anim_run = [0,23]

class Pidgey(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Pidgey, self).__init__(*args, **kwargs)

        self.type = ['normal', 'flying']
        self.model = 'Pidgey_skeleton'
        self.name = 'pidgey'

        # ANIMATION DATA
        self.anim_stand = [0,35]
        self.anim_walk = [0,15]
        self.anim_run = [0,11]

class Oddish(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Oddish, self).__init__(*args, **kwargs)

        self.type = ['grass']
        self.model = 'Oddish_skeleton'
        self.name = 'oddish'

        # ANIMATION DATA
        self.anim_stand = [0,49]
        self.anim_walk = [0,29]
        self.anim_run = [0,17]

class Jigglypuff(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Jigglypuff, self).__init__(*args, **kwargs)

        self.type = ['psyho']
        self.model = 'Jigglypuff_skeleton'
        self.name = 'jigglypuff'

        # ANIMATION DATA
        self.anim_stand = [0,49]
        self.anim_walk = [0,29]
        self.anim_run = [0,19]

class Psyduck(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Psyduck, self).__init__(*args, **kwargs)

        self.type = ['normal', 'flying']
        self.model = 'Psyduck_skeleton'
        self.name = 'psyduck'

        # ANIMATION DATA
        self.anim_stand = [0,49]
        self.anim_walk = [0,29]
        self.anim_run = [0,27]

class Cubone(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Cubone, self).__init__(*args, **kwargs)

        self.type = ['ground']
        self.model = 'Cubone_skeleton'
        self.name = 'cubone'

        # ANIMATION DATA
        self.anim_stand = [0,47]
        self.anim_walk = [0,29]
        self.anim_run = [0,14]

class Scyther(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Scyther, self).__init__(*args, **kwargs)

        self.type = ['grass', 'fight']
        self.model = 'Scyther_skeleton'
        self.name = 'scyther'

        # ANIMATION DATA
        self.anim_stand = [0,59]
        self.anim_walk = [0,29]
        self.anim_run = [0,19]

class Meow(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Meow, self).__init__(*args, **kwargs)

        self.type = ['normal']
        self.model = 'Meow_skeleton'
        self.name = 'meow'

        # ANIMATION DATA
        self.anim_stand = [0,41]
        self.anim_walk = [0,30]
        self.anim_run = [0,16]

class Mewtwo(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Mewtwo, self).__init__(*args, **kwargs)

        self.type = ['normal']
        self.model = 'Mewtwo_skeleton'
        self.name = 'mewtwo'

        # ANIMATION DATA
        self.anim_stand = [0,89]
        self.anim_walk = [0,44]
        self.anim_run = [0,29]

class Pikachu(Pokemon):

    def __init__(self,*args, **kwargs):
        super(Pikachu, self).__init__(*args, **kwargs)

        self.type = ['electric']
        self.model = 'Pikachu_skeleton'
        self.name = 'pikachu'

        # ANIMATION DATA
        self.anim_stand = [0,33]
        self.anim_walk = [0,29]
        self.anim_run = [0,9]


# a = Pokemon(level=2)
# a.get_sound()