from util import hook

@hook.command
def profile(inp):
    ".profile <username> -- links to <username>'s profile on forrst"
    return 'http://forrst.com/people/' + ''.join(inp.split())
