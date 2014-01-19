import os

class EvaluatorStates(object):
    QUIT = 'quit'

class Evaluator(object):
    
    # command tokens
    QUIT_COMMAND_TOKEN = 'quit'    
        
    # command token separator/whitespace
    COMMAND_TOKEN_SEPARATOR = ' '
        
    def __init__(self):
        self.state = { EvaluatorStates.QUIT : False }
        self.commands = { Evaluator.QUIT_COMMAND_TOKEN : self.quit_command }    

    def quit_command(self, params):
        self.state[EvaluatorStates.QUIT] = True  
        return ['quitting']  
        
    def evaluate(self, raw_sequence):
        '''
        deciphers raw sequence to expression,
        evaluates expression,
        returns text line output
        '''  

        tokens = raw_sequence.split(Evaluator.COMMAND_TOKEN_SEPARATOR)
        
        if len(tokens) == 0:
            return []
        
        command_token = tokens[0]
        command_parameters = tokens [1:]        

        output_lines = ['unknown command']

        if command_token in self.commands.keys():
            output_lines = self.commands[command_token](command_parameters)
            
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