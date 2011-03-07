#!/usr/bin/env python
import re
import nltk
import html2text
from nltk.probability import FreqDist 
from nltk.tokenize import RegexpTokenizer
from nltk.metrics import BigramAssocMeasures, spearman_correlation, ranks_from_scores
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
    content = clean_html(input)
    output = SimpleSummarizer().summarize(content, num_sentences)
    if len(output) <= 155:
        return output
    else:
        output = SimpleSummarizer().summarize(content, 1)
        if len(output) > 155:
            return output[:152] + '...'
        else:
            return output

def collocations(input, threshold=3, scorer=None, compare_scorer=None):
    content = clean_html(input)

    if scorer is None:
        scorer = BigramAssocMeasures.likelihood_ratio
    if compare_scorer is None:
        compare_scorer = BigramAssocMeasures.raw_freq

    ignored_words = nltk.corpus.stopwords.words('english')
    word_filter = lambda w: len(w) < 3 or w.lower() in ignored_words or w.isdigit()

    tokenizer = RegexpTokenizer('\w+')
    words = [word.lower()
             for word in tokenizer.tokenize(content)]

    cf = nltk.collocations.BigramCollocationFinder.from_words(words)
    cf.apply_freq_filter(threshold)
    cf.apply_word_filter(word_filter)
    return cf.nbest(scorer, 15)

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

def clean_html(html):
    return ''.join(BeautifulSoup(html).findAll(text=True))
