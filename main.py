def update_state(state, index, result):
    # cannot return state directly because it returns the ref of obj state
    # has to use as method to update instance and return the instance of state
    state.update({"index": index, "result": result})
    return state

def update_error(state, error_msg):
    # same as update_state
    state.update({"result": None, "is_error": True, "error": error_msg})
    return state

class Parser:
    "Represents the collection of the methods and states of the parsing"
    def __init__(self, parser_state_transformer):
        """
        parser_state_transformer -> A parser function
        """
        self.parser_state_transformer = parser_state_transformer
    
    # Parser.run => (parser_state_transformer, target_string) => parser_state_transformer(target_string)
    def run(self, target_string):
        initial_state = {
            "target": target_string,
            "index": 0,
            "result": None,
            "is_error": False,
            "error": None
        }
        return self.parser_state_transformer(initial_state)
    
    def map(self, fun):
        def parser_state(state):
            next_state = self.parser_state_transformer(state)

            if next_state["is_error"]:
                return next_state

            return update_state(next_state, next_state["index"], fun(next_state['result']))
             
        return Parser(parser_state)
    
    def errorMap(self, fun):
        def parser_state(state):
            next_state = self.parser_state_transformer(state)

            if not next_state["is_error"]:
                return next_state

            return update_error(next_state, fun(next_state['error']))
             
        return Parser(parser_state)

# str => s => parser_state => state
def str(s):
    "Parses a string for match if it startswith a target string"

    def parser_state(state):
        from operator import itemgetter

         #  destructuring dict is {target_string, index} = {target, index}
        target_string, index, is_error = itemgetter('target', 'index', 'is_error')(state)

        # if this parser is combined with other that pass a error it return the state and finish.
        if is_error:
            return update_error(state, itemgetter('error')(state))

        if len(target_string) <= 0:
            return update_error(state, "The search pattern is empty.")

        # return if success 
        if target_string[index:].startswith(s):
            return update_state(state, index + len(s), s)
        
        # return if error
        return update_error(state, f'Tried to parse \"{s}\", but got \"{target_string[index:index+10]}\"')
        
    return Parser(parser_state)

# letter => parser_state => state
def letters():
    "Parses a string for match if it startswith a target string"
    print('letter')
    def parser_state(state):
        from operator import itemgetter

         #  destructuring dict is {target_string, index} = {target, index}
        target_string, index, is_error = itemgetter('target', 'index', 'is_error')(state)

        # if this parser is combined with other that pass a error it return the state and finish.
        if is_error:
            return update_error(state, itemgetter('error')(state))

        if len(target_string) <= 0:
            return update_error(state, "The search pattern is empty.")

          # return if success 
        if any(char.isalpha() for char in target_string[index:]):
            import re
            extracted_letters = re.search(r'^[A-Za-z]+', target_string[index:]).group()
            return update_state(state, len(extracted_letters), list(extracted_letters))
        # return if success 
        if target_string[index:].isalpha():
            return update_state(state, index, list(target_string))
        
        # return if error
        return update_error(state, f'Got \"{target_string[index:index+10]}\" that contains characters that arent letters.')
        
    return Parser(parser_state)

# digits => parser_state => state
def digits():
    "Parses a string for match if it startswith a target string"
    print('digit')
    def parser_state(state):
        from operator import itemgetter

         #  destructuring dict is {target_string, index} = {target, index}
        target_string, index, is_error = itemgetter('target', 'index', 'is_error')(state)

        # if this parser is combined with other that pass a error it return the state and finish.
        if is_error:
            return update_error(state, itemgetter('error')(state))

        if len(target_string) <= 0:
            return update_error(state, "The search pattern is empty.")

        # return if success 
        if any(char.isdigit() for char in target_string[index:]):
            import re
            extracted_digits = re.search(r'\d+', target_string[index:]).group()
            return update_state(state, len(extracted_digits), list(extracted_digits))
        
        # return if error
        return update_error(state, f'Got \"{target_string[index:index+10]}\" that contains characters that arent digits.')
        
    return Parser(parser_state)

# sequence_of => parsers => parser_state => state
def sequence_of(parsers):
    "Recieves a list of parsers and parse each of them in a list"

    def parser_state(state):
        results = []
        next_state = state

        for i in range(len(parsers)):
            out = parsers[i]().parser_state_transformer(next_state)

            if next_state["is_error"]:
                return update_error(state, next_state["error"])

            next_state = out
            results.append(next_state["result"])
        
        return update_state(state, next_state["index"], results)

    return Parser(parser_state) 

# choice => parsers => parser_state => state
def choice(parsers):
    "Recieves a list of parsers and parse each of them in a list"

    def parser_state(state):
     
        results = []
        next_state = state

        for parser in parsers:
            try:
                next_state = parser().run(state["target"])
            except:
                next_state = parser.run(state["target"])
            
            if not next_state["is_error"]:
               return update_state(state, next_state["index"], next_state["result"])
        
        return update_error(state, 'couldnt parse')


    return Parser(parser_state) 

if __name__ == '__main__':
    p_str = str('hell')

    p_seq = choice([
        digits,
        str('hell')
    ])

    print(p_seq.run('hello world! 123'))