import re

from BeautifulSoup import BeautifulSoup
from util          import hook, urlnorm, http
from urllib2       import Request

ignore       = ['buttbot']
ignore_hosts = ['youtube.com', 'twitter.com', 'youtu.be']

@hook.regex(r'([a-zA-Z]+://|www\.)[^ ]+')
def show_title(match, nick='', chan='', say=None):
    matched = match.group().encode('utf-8')
    url     = urlnorm.normalize(matched)
    host    = Request(url).get_host()

    if not nick in ignore:
        page, response = http.get_html_and_response(url)
        message        = ''

        if host not in ignore_hosts:
            parser = BeautifulSoup(response)
            title  = parser.title.string.strip()

            if title:
                message = 'URL title: %s' % (title)

        # Shorten URLs that are over 80 characters.
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
