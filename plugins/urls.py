import re
from util import hook, urlnorm, http

ignore = ['buttbot']

@hook.regex(r'([a-zA-Z]+://|www\.)[^ ]+')
def show_title(match, nick='', chan='', say=None):
    url = urlnorm.normalize(match.group().encode('utf-8'))
    if "#" in url:
        url = url.replace("#", "&_escaped_fragment_=")
    if not url in ignore and not nick in ignore:
        page = http.get_html(url)
        title = page.xpath('//title')
        if title and 'youtube' not in url:
            titleList = []
            for i in title:
                if i.text_content():
                    titleList.append(i.text_content().strip())
            if titleList:
                titleList = ''.join(titleList)
                string = "URL title: %s" % (''.join(titleList))
                say(string)
