words_file = open("words_alpha.txt", "r")
filtered_file = open("words_alpha_len3plus.txt", "w")
for line in words_file:
    if len(line.strip()) >= 3:
        filtered_file.write(line)
words_file.close()
filtered_file.close()
