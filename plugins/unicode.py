from util import hook

@hook.command
def print_u(inp):
    string = unicode(inp)
    return string.encode('ascii')
