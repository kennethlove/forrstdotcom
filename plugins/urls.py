import re
import urllib
from util import hook, urlnorm, http

ignore = ['buttbot']

@hook.regex(r'([a-zA-Z]+://|www\.)[^ ]+')
def show_title(match, nick='', chan='', say=None):
    matched = match.group().encode('utf-8')
    url     = urlnorm.normalize(matched)

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
            short_url = http.get(
                'http://is.gd/create.php',
                query_params = {'format': 'simple', 'url': matched}
            )

            # Cheap error checking
            if 'error: please' not in short_url.lower():
                if message:
                    message += ' | Short URL: %s'
                else:
                    message = 'Short URL: %s'

                message = message % (short_url)

        if message:
            say(message)
