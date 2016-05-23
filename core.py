#!/usr/bin/python3
# -*- coding: utf-8 -*- #

# core.py
# Wikipedia Translator
# Created by Nick Gashkov on 22.04.16
# Copyright © 2016 Nick Gashkov. All rights reserved.

"""Wikipedia Translator

Following code implements whole logic of the algorithm.

"""

import urllib.request
import wikipedia

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

class Translator():

    """Translator Class

    Following class contains several public functions to search and translate term, given by user.

    """

    def search_user_term(user_term, user_language):

        """Search User Term Function

        Following function implements search by wikipedia for term, given by user.

        Args:
            user_term (string): term, given by user;
            user_language (string): initial language of the term ('ru'/'en').

        Returns:
            wikipedia.search object: Contains up to 10 search results to adjust query later if necessary.

        """

        wikipedia.set_lang(user_language)

        return wikipedia.search(user_term, results=10)

    def translate_user_term(user_term, user_language):

        """Translate User Term Function

        Following function implements translation of the term, given by user.

        Args:
            user_term (string): term, given by user;
            user_language (string): initial language of the term ('ru'/'en').

        Returns:
            string: Result of the search pushed into string, using following format: '[CODE] [RESULT]', where [CODE] --- code of an execution (either 0 if everything is fine or 1 otherwise) and [RESULT] --- result of an execution (either translated term if it exists or description of an error otherwise).

        """

        try:
            wiki_query = wikipedia.page(user_term)
        except wikipedia.exceptions.DisambiguationError:
            result = '1 Specify your query'
            return result
        except wikipedia.exceptions.PageError:
            result = '1 No page, named ' + user_term
            return result

        html_query = urllib.request.urlopen(wiki_query.url)
        if (user_language == 'en'):
            soap_query = BeautifulSoup(html_query, 'html.parser', parse_only=SoupStrainer('a', lang='ru'))
        else:
            soap_query = BeautifulSoup(html_query, 'html.parser', parse_only=SoupStrainer('a', lang='en'))

        link_to_translation = str(soap_query)
        end_of_link_to_translation = link_to_translation.find('" href')
        formatted_link_to_translation = 'https:' + link_to_translation[9:end_of_link_to_translation]

        try:
            html_translation = urllib.request.urlopen(formatted_link_to_translation)
            soap_translation = BeautifulSoup(html_translation, 'html.parser')
            string_translation = soap_translation.title.string
            if (user_language == 'en'):
                result = '0' + string_translation[:-12]
            else:
                result = '0' + string_translation[:-35]
        except:
            result = '1 No translation for this term'

        return result
