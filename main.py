# str => s => parser_state => state
def str(s):
    "Parses a string for match if it startswith a target string"

    def parser_state(state):
        from operator import itemgetter

        # if this parser is combined with other that pass a error it return the state and finish.
        if(state["isError"]):
            return state

        #  destructuring dict is {target_string, index} = {target, index}
        target_string, index = itemgetter('target', 'index')(state)

        #print( {"s": s, "target": target_string} )
        if (target_string[index:].startswith(s)):
            return {
                "target": target_string,
                "index": index + len(s),
                "result": s,
                "error": None,
                "isError": False
            }
        return {
            "target": target_string,
            "index": index,
            "result": None,
            "isError": True,
            "error": f'Tried to parse \"{s}\", but got \"{target_string[index:index+10]}\"'
        }
    
    return parser_state

# sequence_of => parsers => parser_state => state
def sequence_of(parsers):
    "Recieves a list of parsers and parse each of them in a list"

    def parser_state(state):
        results = []
        next_state = state

        for p in parsers:
            next_state = p(next_state)
            results.append(next_state["result"])
        
        return {
            "target": next_state["target"],
            "index": next_state["index"],
            "result": results,
            "isError": False,
            "error": None
        }
    return parser_state

# run => (parser, target) => parser(target)
def run(parser, target):
    initial_state = {
        "target": target,
        "index": 0,
        "result": None,
        "isError": False,
        "error": None
    }
    return parser(initial_state)

if __name__ == '__main__':
    # parser = sequence_of([str('hello there!'), str('goodbye there')])
    parser = str('azul ')
    print(run(parser, 'hello there!goodbye there'))