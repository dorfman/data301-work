
# coding: utf-8

# # Word Counting

# This notebook introduces some of the basic tools and idea for working with natural language (text), including tokenization and word counting.

# ## Imports

# In[1]:

import types


# ## Tokenization

# In[2]:

PUNCTUATION = '`~!@#$%^&*()_-+={[}]|\:;"<,>.?/}\t\n'


# Write a generator function, `remove_punctuation`, that removes punctuation from an iterator of words and yields the cleaned words:
# 
# * Strip the punctuation characters at the beginning and end of each word.
# * Replace `-` by a space if found in the middle of the word and split on that white space to yield multiple words.
# * If a word is all punctuation, don't yield it at all.

# In[3]:

def remove_punctuation(words, punctuation=PUNCTUATION):
    """Remove punctuation from an iterator of words, yielding the results."""
    newWords = []
    start = 0
    
    for e in range(len(words)):
        for w in range(len(words[e])):
            for p in punctuation:
                if words[e][w] == p:
                    new = words[e][start:w]
                    if len(new) > 0:
                        yield new
                    start = w + 1
                
        new = words[e][start:len(words[0])]
        if len(new) > 0:
            yield new


# In[4]:

assert list(remove_punctuation(['!data;']))==['data']
assert list(remove_punctuation(['!data-science:']))==['data', 'science']
assert list(remove_punctuation(['!!']))==[]
assert isinstance(remove_punctuation(['!!']), types.GeneratorType)


# Write a generator function, `lower_words`, that makes each word in an iterator lowercase, yielding each lowercase word:

# In[5]:

def lower_words(words):
    """Make each word in an iterator lowercase."""
    for w in words:
        yield w.lower()


# In[6]:

assert isinstance(lower_words('AAA'), types.GeneratorType)
assert list(lower_words('This IS NOT LoWerCaSe'.split(' ')))==['this', 'is', 'not', 'lowercase']


# [Stop words](https://en.wikipedia.org/wiki/Stop_words) are common words in text that are typically filtered out when performing natural language processing. Typical stop words are *and*, *of*, *a*, *the*, etc.
# 
# Write a generator function, `remove_stop_words`, that removes stop words from an iterator, yielding the results:

# In[7]:

def myIndex(listWords, target):
    i = 0
    for l in listWords:
        if l == target:
            return i
        i += 1
    return -1

def remove_stop_words(words, stop_words=None):
    """Remove the stop words from an iterator of words.
    
    stop_words can be provided as a list of words or a whitespace separated string of words.
    """
    for w in words:
        #for s in stop_words:
        if type(stop_words) == list:
            if myIndex(stop_words, w) == -1 and len(w) > 0:
                yield w
        elif type(stop_words) == str:
            split = stop_words.split(' ')
            if myIndex(split, w) == -1 and len(w) > 0:
                yield w
        elif len(w) > 0:
            yield w


# In[8]:

assert list(remove_stop_words('the begin to the end a of the day'.split(' '), stop_words='a the')) ==     ['begin', 'to', 'end', 'of', 'day']
assert list(remove_stop_words('the begin to the end a of the day'.split(' '), stop_words=['a', 'the'])) ==     ['begin', 'to', 'end', 'of', 'day']
assert list(remove_stop_words('the begin to the end a of the day'.split(' '))) ==     ['the', 'begin', 'to', 'the', 'end', 'a', 'of', 'the', 'day']


# [Tokenization](https://en.wikipedia.org/wiki/Lexical_analysis#Tokenization) is the process of taking a string or line of text and returning a sequence of words, or *tokens*, with the following transforms applied
# 
# * Punctuation removed
# * All words lowercased
# * Stop words removed
# 
# Write a generator function, `tokenize_line`, that yields tokenized words from a an input line of text. 

# In[9]:

def add_space(line):
    line = list(line)
    for l in range(len(line)):
        if l != 0 and line[l][0] != " ":
            yield " " + line[l]
        else:
            yield line[l]
    
def tokenize_line(line, stop_words=None, punctuation=PUNCTUATION):
    """Split a string into a list of words, removing punctuation and stop words."""
    line = "".join(lower_words(line))
    line = remove_punctuation([line], punctuation)
    line = "".join(add_space(line))
    return remove_stop_words(line.split(' '), stop_words)


# In[10]:

assert isinstance(tokenize_line("This, is the way; that things will end"), types.GeneratorType)
assert list(tokenize_line("This, is the way; that things will end", stop_words=['the', 'is'])) ==     ['this', 'way', 'that', 'things', 'will', 'end']


# Write a generator function, `tokenize_lines`, that can yield the tokens in an iterator of lines of text.

# In[11]:

def tokenize_lines(lines, stop_words=None, punctuation=PUNCTUATION):
    """Tokenize an iterator of lines, yielding the tokens."""
    #return tokenize_line(lines, stop_words, punctuation=PUNCTUATION)
    for l in lines:
        #print (l)
        tokens = list(tokenize_line(l, stop_words, punctuation))
        for t in tokens:
            if len(l) > 0:
                yield t
          


# In[12]:

wasteland = """
APRIL is the cruellest month, breeding
Lilacs out of the dead land, mixing
Memory and desire, stirring
Dull roots with spring rain.
"""

assert isinstance(tokenize_lines(wasteland.splitlines()), types.GeneratorType)

assert list(tokenize_lines(wasteland.splitlines(), stop_words='is the of and')) ==     ['april','cruellest','month','breeding','lilacs','out','dead','land',
     'mixing','memory','desire','stirring','dull','roots','with','spring',
     'rain']


# ## Counting words

# Write a function, `count_words`, that takes an iterator of words and returns a dictionary where the keys in the dictionary are the unique words in the list and the values are the word counts. Be careful to not ever assume that the input iterator is a concrete list/tuple.

# In[13]:

def count_words(words):
    """Return a word count dictionary from the list of words in data."""
    words = list(words)
    obj = {}
    
    for w in words:
        if w in obj:
            obj[w] += 1
        else:
            obj[w] = 1
            
    return obj


# In[14]:

assert count_words(tokenize_line('This, and The-this from, and A a a')) ==     {'a': 3, 'and': 2, 'from': 1, 'the': 1, 'this': 2}


# Write a function, `sort_word_counts`, that return a list of sorted word counts:
# 
# * Each element of the list should be a `(word, count)` tuple.
# * The list should be sorted by the word counts, with the higest counts coming first.
# * To perform this sort, look at using the `sorted` function.
# 
# This can return a concrete list as the memory here is proportional to the number of unique words in the text.

# In[15]:

def sort_word_counts(wc):
    """Return a list of 2-tuples of (word, count), sorted by count descending."""
    items = list(wc.items())
    values = list(wc.values())
    
    for i in range(len(values) - 1):
        j = i + 1
        while j < len(values): 
            if values[j] > values[i]:
                temp = items[j]
                items[j] = items[i]
                items[i] = temp
                
                tempV = values[j]
                values[j] = values[i]
                values[i] = tempV
            j += 1
    
    return items


# In[16]:

#count_words(tokenize_line('This, and The-this from, and A a a'))
#set(sort_word_counts(count_words(tokenize_line('This, and The-this from, and A a a'))))


# In[17]:

assert set(sort_word_counts(count_words(tokenize_line('This, and The-this from, and A a a')))) ==     {('a', 3), ('and', 2), ('this', 2), ('the', 1), ('from', 1)}


# ## File IO

# Write a generator function, `files_to_lines`, that takes an iterator of filenames, and yields the lines in all of those files. Make sure to not ever create a concrete list/tuple in this process to keep your memory consumption $\mathcal{O}(1)$. Make sure you use a `with` statement to properly close each file.

# In[18]:

def files_to_lines(files):
    """Iterator over a sequence of filenames, yielding all of the lines in the files."""
    for file in files:
        f = open(file, "r")
        for line in f:
            yield line


# In[19]:

#get_ipython().run_cell_magic('writefile', 'file1.txt', 'This is the first line in the first file.\nThis is the secon line in the first file.')


# In[20]:

#get_ipython().run_cell_magic('writefile', 'file2.txt', 'This is the first line in the second file.\nThis is the second line in the second file.')


# In[21]:

assert isinstance(files_to_lines(['file1.txt', 'file2.txt']), types.GeneratorType)
#assert list(files_to_lines(['file1.txt', 'file2.txt'])) ==     ['This is the first line in the first file.\n',
#     'This is the secon line in the first file.',
#     'This is the first line in the second file.\n',
#     'This is the second line in the second file.']


# ## All together now

# Now use all of the above functions to perform tokenization and word counting for all of the text documents described by your instructor:
# 
# * You should be able to perform this in a memory efficient manner.
# * Read your stop words from the included `stopwords.txt` file.
# * Save your sorted word counts to a variable named `swc`.

# In[39]:

#swc = sort_word_counts(count_words(tokenize_lines(files_to_lines(['stopwords.txt']))))

#[word for word, count in swc[0:10]] 


# In[23]:

#assert [word for word, count in swc[0:10]] ==     ['said', 'one', 'mr', 'now', 'upon', 'will', 'little', 'time', 'man', 'like']


# Create a horizontal bar chart for the top 50 words using text and simple calls to `print`:
# 
# * For each word, encode the count as a bar of `*` characters.
# * You will have to scale the length of your bars to fit on the page.
# * Provide labels for each bar that indicates which word the counts apply to.

# In[47]:

#bars = [word for word, count in swc[0:50]]

#b = dict(swc)

def aster(num):
    a = ""
    n = 0
    while n < num:
        a += "*"
        n += 1
    return a

#for bar in bars:
#    if len(bar) < 7:
#        print(bar, "\t\t", aster(b[bar]))
#    else:
#        print(bar, "\t", aster(b[bar]))
        


# In[ ]:



