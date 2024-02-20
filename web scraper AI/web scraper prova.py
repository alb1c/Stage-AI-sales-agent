import nltk
import requests
from bs4 import BeautifulSoup
from nltk import BigramCollocationFinder
from nltk.tokenize import RegexpTokenizer

url = 'https://volcanicminds.com'
# url = 'https://www.gutenberg.org/files/42671/42671-h/42671-h.htm'


# Make the request and check object type
r = requests.get(url)

# Extract HTML from Response object and print
html = r.text

# Create a BeautifulSoup object from the HTML
soup = BeautifulSoup(html, "lxml")

# extracting all the text from the page
wholeText = soup.getText()

print(wholeText)

urlSet = set()
urlSet.add(url)

header = soup.find('head')
for link in soup.find_all('a'):
    linkAsText = str(link.get('href'))
    # print(linkAsText)
    if linkAsText.startswith('/') and len(linkAsText) > 2:
        print(linkAsText)
        urlStr = url + linkAsText
        print(urlStr)
        urlSet.add(urlStr)

print(urlSet)

for link in urlSet:
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    text = soup.getText()
    wholeText = wholeText + '\n' + text

# Create tokenizer
tokenizer = RegexpTokenizer('\w*')

# Create tokens
tokens = tokenizer.tokenize(wholeText)

# Initialize new list
words = []

# Loop through list tokens and make lower case
for word in tokens:
    if len(word) > 1:
        words.append(word.lower())

# Get English stopwords and print some of them
sw = nltk.corpus.stopwords.words('italian')

# Initialize new list
words_ns = []

# Add to words_ns all words that are in words but not in sw
for word in words:
    if word not in sw:
        words_ns.append(word)

# Create freq dist and plot
freqdist1 = nltk.FreqDist(words_ns)
freqdist1.plot(25)

print('tokens: ', tokens)
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(words_ns)
finder.apply_word_filter(lambda w: str(w).isnumeric())
scored = finder.score_ngrams(bigram_measures.raw_freq)
print(sorted(bigram for bigram, score in scored))


# freqdist2 = nltk.FreqDist(nltk.collocations(wholeText))
