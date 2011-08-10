from util import hook
from random import randrange, randint, choice

@hook.command
def dick(inp, say=None):
    shaft = '='*randrange(0, 10)
    dick = '8%sD' % shaft
    if inp:
        dick = '%s~~~ %s' % (dick, inp)
    return dick

@hook.command
def vag(inp):
    return "{()}"

@hook.command
def boobs(inp, say=None):
    nipples = choice('oO0')
    boobs = "( {nipple} Y {nipple} )".format(
        nipple=nipples
    )
    return boobs

@hook.command
def booty(inp):
    return '(_|_)'
