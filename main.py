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

# sequence_of => parsers => parser_state => state
def sequence_of(parsers):
    "Recieves a list of parsers and parse each of them in a list"

    def parser_state(state):
        results = []
        next_state = state

        for p in parsers:
            if next_state["is_error"]:
                return update_error(state, next_state["error"])
            
            next_state = p.parser_state_transformer(next_state)
            results.append(next_state["result"])
        
        return update_state(state, next_state["index"], results)

    return Parser(parser_state) 

if __name__ == '__main__':
    parser = sequence_of([str('hello there!'), str('goodbye there')])
    p_str = str('azul ').map(lambda x: {"value": x.upper()}).errorMap(lambda x: {"error": x})
    print(p_str.run('hello there!goodbye there'))
    # p_seq = sequence_of([str('hello there!'), str('goodbye there')])
    # print(p_seq.run('hello there!goodbye there'))