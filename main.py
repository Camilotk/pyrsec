
# str => s => target
def str(s):
    "Parses a string for match if it startswith a target string"
    def target(t_str):
        if (t_str.startswith(s)):
            return s
        return Exception('Tried to parse but got')
    return target

def run(parser, target):
    return parser(target)

if __name__ == '__main__':
    parser = str('hello there!')
    print(run(parser, 'hellthere!'))