import bge

def run(cont):
    '''
    Listens to messages waiting for the signal to start a game
    or to reset the level progress.
    '''
    message_sens = cont.sensors['Message']
    for message in message_sens.subjects:
        if message == 'START':
            #Starts the level loading process
            start_game()
        elif message == 'RESET':
            #Resets the game progress so the player starts at the first level
            reset_progress()

def start_game():
    bge.logic.addScene('Base', 1)
    bge.logic.addScene('Loading', 1)
    bge.logic.getCurrentScene().end()

def reset_progress():
    '''
    The file progress.cfg contains a number representing the current position
    in the game. This function resets it to 0
    '''
    set_progress(0)
    print('Level File Reset')

def set_progress(num):
    '''
    writes to the progress file with the number fed into it.
    Also valid input is 'next' which will increment the number by 1
    '''
    path = bge.logic.expandPath('//progress.cfg')
    if num == 'next':
        #Increment the number by 1
        current_progress = open(path).read()
        num = int(current_progress)+1
    progress_file = open(path, 'w')
    progress_file.write(str(num))
    progress_file.close()
