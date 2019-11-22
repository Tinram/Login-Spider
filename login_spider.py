#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Log-In Spider-Parser """


import sys
from StringIO import StringIO
from time import time as timer
from multiprocessing.dummy import Pool as ThreadPool
from HTMLParser import HTMLParser
import pycurl



## CONFIG ##
BASE_URL = 'http://example.com'
LOGIN_PAGE = 'http://example.com/login.php'
FORM_POST = 'username=user@example.com&password=password&action=login' # customise according to log-in form HTML
COOKIE_FILE = 'cookie.txt'
LOGIN_TOKEN = 'Welcome' # string token present in page source on successful login
REMOVE_QUERY_STRING = True
EXCLUSIONS = ('www', 'javascript', '.pdf', 'mailto:')
LINKS = []
NUMBER_THREADS = 16
NEEDLE = 'xdebug'
##



class LoginSpider(object):

    """
        Login Spider: threaded log-in spider-parser.
        Log-in to a website, harvest links in pages, then process them (currently, scan page content for a string).

        Usage              python login_spider.py

        Python Version     2.7
        Author             Martin Latter
        Copyright          Martin Latter 04/12/2017
        Version            0.06
        Credits            jfs and philshem (pool threading)
        License            GNU GPL version 3.0 (GPL v3); http://www.gnu.org/licenses/gpl.html
        Link               https://github.com/Tinram/Login-Spider.git
    """


    needle_found = False


    def __init__(self):

        """ Initialise and execute methods. """

        login_page_html = self.log_in(LOGIN_PAGE)
        self.parse_page(login_page_html)
        self.process_links()


    def log_in(self, url):

        """
            Attempt to log-in through website form and return page content.
            Args:
                url: log-in page
        """

        buf = StringIO()

        ch = pycurl.Curl()
        ch.setopt(ch.URL, url)
        ch.setopt(pycurl.TIMEOUT, 10)
        ch.setopt(pycurl.FOLLOWLOCATION, 1)
        ch.setopt(pycurl.POSTFIELDS, FORM_POST)
        ch.setopt(pycurl.COOKIEJAR, COOKIE_FILE)
        ch.setopt(pycurl.COOKIEFILE, COOKIE_FILE)
        #ch.setopt(ch.VERBOSE, True)
        ch.setopt(pycurl.SSL_VERIFYPEER, 0)
        ch.setopt(ch.WRITEFUNCTION, buf.write)
        ch.perform()
        ch.close()

        html = buf.getvalue()

        if LOGIN_TOKEN in html:
            print '\n found "' + LOGIN_TOKEN + '" token, now logged-in via ' + LOGIN_PAGE
        else:
            print '\n ** could not log-in through ' + LOGIN_PAGE + ' **\n'
            sys.exit(1)

        return html


    def parse_page(self, html):

        """
            Parse the log-in page and extract links.
            Args:
                html: log-in page content
        """

        parser = LinkParser()
        parser.feed(html)

        if not len(LINKS):
            print '\n no links extracted from log-in page\n'
            sys.exit(1)

        print '\n %i links found in first page ...' % len(LINKS)

        start = timer()
        pool = ThreadPool(NUMBER_THREADS)
        results = pool.imap_unordered(self.parse_page_links, LINKS)
        pool.close()
        pool.join()

        print '\n %i links found in spidered pages' % len(LINKS)
        print '\n link searches: %s secs\n' % str.format('{0:.3f}', (timer() - start))

        #for x in LINKS:
            #print x


    def parse_page_links(self, lnk):

        """
            Check URL access.
            Args:
                lnk: link
        """

        buf = StringIO()

        ch = pycurl.Curl()
        ch.setopt(ch.URL, lnk)
        ch.setopt(pycurl.TIMEOUT, 10)
        ch.setopt(pycurl.FOLLOWLOCATION, 1)
        ch.setopt(pycurl.COOKIEJAR, COOKIE_FILE)
        ch.setopt(pycurl.COOKIEFILE, COOKIE_FILE)
        ch.setopt(pycurl.SSL_VERIFYPEER, 0)
        ch.setopt(ch.WRITEFUNCTION, buf.write)
        ch.perform()
        ch.close()

        html = buf.getvalue()
        parser = LinkParser()
        parser.feed(html)


    def process_links(self):

        """ Set-up the page parsing from the collected links. """

        start = timer()
        pool = ThreadPool(NUMBER_THREADS)
        results = pool.imap_unordered(self.search_page, LINKS)
        pool.close()
        pool.join()

        if not self.needle_found:
            print "\n '" + NEEDLE + "' not found in spidered pages\n"

        print '\n file searches: %s secs\n' % str.format('{0:.3f}', (timer() - start))


    def search_page(self, lnk):

        """
            Search page content for the string specified in NEEDLE.
            Args:
                lnk: link
        """

        buf = StringIO()

        ch = pycurl.Curl()
        ch.setopt(ch.URL, lnk)
        ch.setopt(pycurl.TIMEOUT, 10)
        ch.setopt(pycurl.FOLLOWLOCATION, 1)
        ch.setopt(pycurl.COOKIEJAR, COOKIE_FILE)
        ch.setopt(pycurl.COOKIEFILE, COOKIE_FILE)
        ch.setopt(pycurl.SSL_VERIFYPEER, 0)
        ch.setopt(ch.WRITEFUNCTION, buf.write)
        ch.perform()
        ch.close()

        html = buf.getvalue()

        if NEEDLE in html:
            self.needle_found = True
            print '+ ' + str(lnk)

# end class


class LinkParser(HTMLParser):

    """
        HTMLParser with a link filter.
    """

    def handle_starttag(self, tag, attrs):

        """
            Process HTML tag.
            Args:
                tag: tag
                attrs: tag's attributes
        """

        if tag == 'a':

            for name, value in attrs:

                if name == 'href':

                    if any(s in value for s in EXCLUSIONS):
                        continue
                    elif value[0] == '/':
                        tmp = BASE_URL + value
                    elif value[0:3] != 'http':
                        tmp = BASE_URL + '/' + value
                    else:
                        tmp = value

                    if REMOVE_QUERY_STRING:
                        if '?' in tmp:
                            tmp = tmp.split('?')
                            tmp = tmp[0]

                    if tmp not in LINKS:
                        LINKS.append(tmp)

# end class



def main():

    """ Invoke class. """

    LoginSpider()


if __name__ == '__main__':

    main()
