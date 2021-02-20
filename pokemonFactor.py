from bge import logic, types, events, constraints
import random
import os

scene = logic.getCurrentScene()

SPAWNERS = {
    "forest" : scene.objects['Forest_Spawner']
}


class PokemonFactory():

    def __init__(self):
        pass
