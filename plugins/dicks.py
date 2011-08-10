from util import hook
from random import randrange

@hook.command
def dicks(inp, say=None):
	string = '8%sD~~~ %s ~~~C%s8' % ('='*randrange(0, 15), inp, '='*randrange(0, 15))
	say(string)
