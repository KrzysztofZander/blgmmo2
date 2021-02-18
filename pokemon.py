
class Pokemon():

    def __init__(self, *args , **kwargs):
        
        self.name = **kwargs['name']
        self.level = **kwargs['level']
        self.type = **kwargs['type']
        self.model = **kwargs['model']

    
    def initialize_model(self):
        pass
        
