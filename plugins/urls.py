import re
from util import hook, urlnorm, http

ignore = ['buttbot']
is_gd  = 'http://is.gd/create.php?format=simple&url=%s'

@hook.regex(r'([a-zA-Z]+://|www\.)[^ ]+')
def show_title(match, nick='', chan='', say=None):
    url     = urlnorm.normalize(match.group().encode('utf-8'))

    if not url in ignore and not nick in ignore:
        page, response = http.get_html_and_response(url)
        title          = page.xpath('//title')
        message        = ''

        # Only ignore URLs of which "twitter" or "youtube" is part of the
        # domain and not just part some some URI segment.
        if 'youtube.' not in url and 'twitter.' not in url:
            # Don't show the title if there isn't one
            if title:
                titleList = []
                short_url = 'Not Found'

                for i in title:
                    if i.text_content():
                        titleList.append(i.text_content().strip())

                if titleList:
                    titleList = ''.join(titleList)
                    message   = 'URL title: %s' % (''.join(titleList))

        if len(url) >= 80:
            # Get the short URL.
            short_url = http.get(is_gd % (url))

            # Cheap error checking
            if 'error: please' not in short_url.lower():
                if message:
                    message += ' | Short URL: %s'
                else:
                    message = 'Short URL: %s'

                message = message % (short_url)

        if message:
            say(message)
