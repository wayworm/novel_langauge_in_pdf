
def CHATGPT_extract_non_frequent(words, frequency_list_dir):
    # Read all lines from the file and strip whitespace
    with open(frequency_list_dir, 'r') as corpus_file:
        frequent_words = set(line.strip() for line in corpus_file)

    # Filter out words that are in the frequent words list
    non_frequent = [word for word in words if word not in frequent_words]

    print("extract_non_frequent")
    return non_frequent


words_written = open("words.txt","r")

words = words_written.readlines()
words = [word[:-1] for word in words]


non_frequent = CHATGPT_extract_non_frequent(words, "20k.txt")

print(non_frequent)