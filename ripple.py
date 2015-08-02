# ripple - python3 repl skeleton @ david barkhuizen Jan 2014

# python3 check
#
import sys
(major_version_number, minor_version_number, a, b, c) = sys.version_info
if major_version_number < 3 :
    print('python 3 required')
    sys.exit(1)

import os

class Command(object):
    def __init__(self, token, function, description = None):
        '''init

        token
        - will be lowercased

        function
        - takes a list of parameters
        - returns a string list for screen display
        '''
        
        self.token = token.lower().strip()
        self.function = function
        self.description = description

class EvaluatorStates(object):
    QUIT = 'quit'

# define commands here
#
import_commands = []

class Evaluator(object):
    
    SEPARATOR_TOKEN = ' '
    
    def __init__(self):
        
        self.state = { EvaluatorStates.QUIT : False }        
        
        self.commands = {}

        quit_cmd = Command('quit', self.quit_command_fn)
        exit_cmd = Command('exit', self.quit_command_fn)
        list_cmd = Command('list', self.list_command_fn)
        help_cmd = Command('help', self.help_command_fn)

        commands = [quit_cmd, exit_cmd, list_cmd, help_cmd]
        commands.extend(import_commands)

        for command in commands:
            self.commands[command.token] = command

    def help_command_fn(self, params = None):
        return ['no can hear you scream']

    def list_command_fn(self, params = None):
        return sorted([x.token + (' - ' + x.description if x.description is not None else '') for x in self.commands.values()])

    def quit_command_fn(self, params = None):
        self.state[EvaluatorStates.QUIT] = True  
        return ['quitting...']  
        
    def evaluate(self, raw_sequence):
        '''
        deciphers raw sequence to expression,
        evaluates expression,
        returns text line output
        '''  

        tokens = raw_sequence.split(Evaluator.SEPARATOR_TOKEN)
        
        if len(tokens) == 0:
            return []
        
        command_token = tokens[0]
        command_parameters = tokens[1:]        

        output_lines = ['unknown command']

        if command_token in self.commands.keys():
            output_lines = self.commands[command_token].function(command_parameters)
            
        return output_lines

def clear_terminal():
    print(chr(27) + "[2J")

def xprint(output_lines):

    WINDOW_HEIGHT, WINDOW_WIDTH = os.popen('stty size', 'r').read().split()
    
    WINDOW_HEIGHT = int(WINDOW_HEIGHT) - 4
    WINDOW_WIDTH = int(WINDOW_WIDTH)
    
    clear_terminal()
    
    # print output
        
    print(('-' * WINDOW_WIDTH))
    
    visible_lines = output_lines[:min([len(output_lines), WINDOW_HEIGHT])]
    
    for visible_line in visible_lines:
        visible_segment = visible_line[:min([len(visible_line), WINDOW_WIDTH])]
        print(visible_segment)

    if (len(visible_lines) < WINDOW_HEIGHT):
        print('\n' * (WINDOW_HEIGHT - len(visible_lines)))
        
    print(('-' * WINDOW_WIDTH))
       
    
def xread():
    '''
    returns None if user has requested to escape
    '''      
    raw = input('? ')
    return raw

def repl(evaluator=None):
    
    if evaluator == None:
        evaluator = Evaluator()
    
    welcome_message = 'type a command and hit enter.  quit to Quit, list to list the available commands'
    xprint([welcome_message])
    raw_sequence = ''
    escape = False
    
    # REPL
    #
    while (evaluator.state[EvaluatorStates.QUIT] != True):
        
        # read
        #
        raw_sequence = xread()
        
        # evaluate
        #
        output_lines = evaluator.evaluate(raw_sequence)
        
        # print
        #
        xprint(output_lines)
        
    clear_terminal()

if __name__ == '__main__':
    repl()