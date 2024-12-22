# The aim of this project is to read in the text from some given pdf document and returns definitions of the 
# most commonly used (novel) language in the text.
# I'm defining novel langauge is defined as words not contained within the 20,000 most common english words.
# word list comes from https://github.com/first20hours/google-10000-english


#In it's current form the program prints a list of infrequent words from the provides document.

# Issues:
# - The printed list does not contain all terms that would be considered infrequent.
#           - This may be do to the ad-hoc way in which I was converting text into a list of words.

# The program is very slow, taking around 30-60 seconds for a 2 page, non-text heavy, pdf.
#           - This is limited by the speed of the pyenchant Dict.check() method.

# The program does not currently return definitions like I intend it to.


import enchant
from pypdf import PdfReader


broker = enchant.Broker()
langs = broker.list_languages()


def pdf_page_textExtractor(file_name):

    doc = PdfReader(file_name)
    pages = []
    for page in doc.pages:
        pages.append(page.extract_text())

    print("pdf_page_textExtractor")
    return pages
    

def page_text_cleaner(pages):

    for i in range(len(pages)):
        pages[i] = pages[i].replace(u'\xa0', u' ')
        pages[i] = pages[i].replace('\n', ' ')
        pages[i] = pages[i].replace(u'\uf0b7', ' ')
        pages[i] = pages[i].split(" ")
        try:
            pages[i].remove('')
        except:
            pass
    print("page_text_cleaner")
    return pages


def word_extractor(languages,pages):
    words = []
    number = 0
    for page in pages:
        for word in page:
            number += 1

    counter = 0
    for language in languages:
        for page in pages:
            for word in page:
                try:
                    if enchant.Dict(language).check(word) == True:
                        words.append(word)
                except: 
                    pass
                counter += 1
                if counter % 50 == 0:
                    print( (counter/number)*100, "done")

    words_no_duplicates = list(dict.fromkeys(words))
    words_no_duplicates = [x.lower() for x in words_no_duplicates]

    #punctuation removal
    for word in words_no_duplicates:
        if word[-1] == "." or word[-1] == ",":
            words_no_duplicates[words_no_duplicates.index(word)] = words_no_duplicates[words_no_duplicates.index(word)][:-1]


    print("word_extractor")
    return words_no_duplicates


def extract_non_frequent(words, frequency_list_dir):
    # Read all lines from the file and strip whitespace
    with open(frequency_list_dir, 'r') as corpus_file:
        frequent_words = set(line.strip() for line in corpus_file)

    # Filter out words that are in the frequent words list
    non_frequent = [word for word in words if word not in frequent_words]

    print("extract_non_frequent")
    return non_frequent




# Selecting pdf
pages = pdf_page_textExtractor('A-Beginner’s-Guide-to-Overwatch-Heroes.pdf')

#extracting the words in the file
clean_pages = page_text_cleaner(pages)
words_on_pages = word_extractor(["en_GB"], clean_pages)

#writing them for reference and testing
# words_written = open("words.txt","w")

# for i in words_on_pages:
#     words_written.writelines(i +"\n")

#The final list
non_frequent = extract_non_frequent(words_on_pages, "20k.txt")

print(non_frequent)





# Doesn't work, kept as reference

# def extract_non_frequent(words, frequency_list_dir):
#     #read from file
#     corpus_file = open(frequency_list_dir)

#     non_frequent = words
#     for i in words:
#         for line in corpus_file.readlines():
#             if i == line:
#                 print("removing" , i)
#                 non_frequent.remove(i)

#     print("extract_non_frequent")
#     return words

