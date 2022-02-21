
# str => s => target
def str(s):
    "Parses a string for match if it startswith a target string"

    def parser_state(state):
        from operator import itemgetter

        #  destructuring dict is {target_string, index} = {target, index}
        target_string, index = itemgetter('target', 'index')(state)

        #print( {"s": s, "target": target_string} )
        if (target_string[index:].startswith(s)):
            return {
                "target": target_string,
                "index": index + len(s),
                "result": s,
            }
        return Exception(f'Tried to parse {s} but got {target_string[index:index+10]}')
    
    return parser_state

def sequence_of(parsers):
    def parser_state(state):
        results = []
        next_state = state

        for p in parsers:
            next_state = p(next_state)
            results.append(next_state["result"])
        
        return {
            "result": results
        }
    return parser_state


def run(parser, target):
    initial_state = {
        "target": target,
        "index": 0,
        "result": None
    }
    return parser(initial_state)

if __name__ == '__main__':
    parser = sequence_of([str('hello there!'), str('goodbye there')])
    # parser = str('hello ')
    print(run(parser, 'hello there!goodbye there'))