"""
remember.py: written by Scaevolus 2010
"""

from util import hook


def db_init(db):
    db.execute("create table if not exists memory(chan, word, data, nick,"
               " primary key(chan, word))")
    db.commit()


def get_memory(db, chan, word):
    row = db.execute("select data from memory where chan=? and word=lower(?)",
                      (chan, word)).fetchone()
    if row:
        return row[0].split(' ', 1)[-1]
    else:
        return None


@hook.command
def remember(inp, nick='', chan='', db=None):
    ".remember <word> <data> -- maps word to data in the memory"
    db_init(db)

    try:
        head, tail = inp.split(None, 1)
    except ValueError:
        return remember.__doc__

    data = get_memory(db, chan, head)
    db.execute("replace into memory(chan, word, data, nick) values"
               " (?,lower(?),?,?)", (chan, head, head + ' ' + tail, nick))
    db.commit()
    if data:
        return 'forgetting "%s", remembering this instead.' % \
                data.replace('"', "''")
    else:
        return 'done.'


@hook.command
def forget(inp, chan='', db=None):
    ".forget <word> -- forgets the mapping that word had"

    db_init(db)
    data = get_memory(db, chan, inp)

    if not chan.startswith('#'):
        return "I won't forget anything in private."

    if data:
        db.execute("delete from memory where chan=? and word=lower(?)",
                   (chan, inp))
        db.commit()
        return 'forgot `%s`' % data.replace('`', "'")
    else:
        return "I don't know about that."


#@hook.regex(r'^\? ?(\S+) ?@?(.+)')
#def question(inp, chan='', say=None, db=None):
#    "?<word> -- shows what data is associated with word"
#    db_init(db)
#    match = len(inp.group().split(' '))
#    if match == 2:
#        word = inp.group(1).strip()
#        sayto = inp.group(2).strip()
#    elif match == 1:
#        sayto = ''
#        word = inp.group().strip().split('?')[-1]
#
#    data = get_memory(db, chan, word)
#    if data:
#        if sayto:
#            data = ': '.join([sayto, data])
#        say(data)

@hook.regex(r'^\? ?(\S+) ?(@?)(.+)$')
def question(inp, chan='', say=None, db=None, to_nick=False):
    "?<word> -- shows what data is associated with word"
    db_init(db)
    match = len(inp.group().split(' '))
    if match >= 2:
        trigger = inp.group(1).strip()
        words = inp.group(3).strip()
        if '@' in inp.group(2).strip():
            to_nick = True
    elif match == 1:
        trigger = inp.group().strip().split('?')[-1]
        words = ''
    data = get_memory(db, chan, trigger)
    if data:
        if words:
            if to_nick:
                data = ' '.join([data, words])
            else:
                data = ': '.join([words, data])
        say(data)
