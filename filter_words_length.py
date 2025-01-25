words_file = open("wordlist.txt", "r")
filtered_file = open("wordlist_filtered.txt", "w")
for line in words_file:
    word = line.strip()
    if len(word) >= 3 and word.isalpha():
        filtered_file.write(line)
words_file.close()
filtered_file.close()
