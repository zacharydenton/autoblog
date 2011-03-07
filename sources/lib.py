#!/usr/bin/env python
import re
import nltk
import html2text
from nltk.probability import FreqDist 
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk.data

from BeautifulSoup import BeautifulSoup


class SimpleSummarizer:
    def reorder_sentences( self, output_sentences, input ):
        output_sentences.sort( lambda s1, s2:
            input.find(s1) - input.find(s2) )
        return output_sentences
    
    def summarize(self, input, num_sentences ):
        # TODO: allow the caller to specify the tokenizer they want
        # TODO: allow the user to specify the sentence tokenizer they want

        tokenizer = RegexpTokenizer('\w+')
        
        # get the frequency of each word in the input
        base_words = [word.lower().encode('utf-8')
            for word in tokenizer.tokenize(input)]
        words = [word for word in base_words if word not in stopwords.words()]
        word_frequencies = FreqDist(words)
        
        # now create a set of the most frequent words
        most_frequent_words = [pair[0] for pair in 
            word_frequencies.items()[:100]]

        # break the input up into sentences.  working_sentences is used 
        # for the analysis, but actual_sentences is used in the results
        # so capitalization will be correct.
        
        actual_sentences = nltk.tokenize.sent_tokenize(input)
        working_sentences = [sentence.lower() 
            for sentence in actual_sentences]

        # iterate over the most frequent words, and add the first sentence
        # that inclues each word to the result.
        output_sentences = []

        for word in most_frequent_words:
            for i in range(0, len(working_sentences)):
                if (word in working_sentences[i] 
                  and actual_sentences[i] not in output_sentences):
                    output_sentences.append(actual_sentences[i])
                    break
                if len(output_sentences) >= num_sentences: break
            if len(output_sentences) >= num_sentences: break
            
        # sort the output sentences back to their original order
        output_sentences = self.reorder_sentences(output_sentences, input)

        # concatinate the sentences into a single string
        return ' '.join(output_sentences)

def summarize(input, num_sentences=2):
    content = ''.join(BeautifulSoup(input).findAll(text=True))
    return SimpleSummarizer().summarize(content, num_sentences)

def html2markdown(input):
    markdown_converter = html2text._html2text(None, '')
    markdown_converter.feed(input)
    markdown_converter.feed('')
    return markdown_converter.outtext

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata
    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)


