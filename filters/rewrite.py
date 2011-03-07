#!/usr/bin/env python
import urllib, urllib2
import nltk
import json
from api import Filter

class GoogleTranslateFilter(Filter):
    '''
    Rewrites text by translating it a number of times.

    E.g. English->German->English will yield a slightly different text.
    '''
    def __init__(self, *languages):
        self.languages = languages

    def filter(self, input):
        output = input
        try:
            for language in self.languages:
                output = self.translate(output, language)
            return output
        except Exception as e:
            print e
            return input

    def translate(self, input, language, fmt='html'):
        output = ''
        api = "https://www.googleapis.com/language/translate/v2"
        api_key = "AIzaSyBgBlJCogk_1Hd_7WaLQgLVbQss0_dvNUc"
        parameters = urllib.urlencode({
            'target': language,
            'format': fmt,
            'key': api_key,
            'q': input.encode('utf-8')
        })
   
        headers= {'X-HTTP-Method-Override': 'GET'}
        request = urllib2.Request(api, parameters, headers)
        response = urllib2.urlopen(request)
        translations = json.loads(response.read())
  
        translated_text = translations['data']['translations'][0]['translatedText']
        output += translated_text
        return output
