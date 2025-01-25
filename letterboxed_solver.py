# input: 4 groups of 3 letters: WHI ESD LAK BNO (order doesn't matter)
# construct trie
# DFS
# for each letter:
#   for each letter on other sides:
#       add that letter to used set
#       if completes a word:
#           if word was already played: fail
#           also fail if word hasn't used any new letters since the last time we started with that letter
#           if all letters used: success
#           else: recurse starting new word with that letter
#           (keep going to next in case of subword e.g. COUNTER/COUNTERPART)
#       if valid options with that letter added:
#           recurse with that letter added
# look at all successes, select fewest words then shortest total words length

dictionary = {}
end = None
max_words = 5

def build_dictionary():
    words_file = open("wordlist_filtered.txt", "r")
    for line in words_file:
        word = line.strip().upper()
        current_node = dictionary
        for letter in word:
            current_node = current_node.setdefault(letter, {})
        current_node[end] = end

def create_bool_list(groups, val):
    bool_list = []
    for group_i in range(len(groups)):
        group_list = []
        for _ in range(len(groups[group_i])):
            group_list.append(val)
        bool_list.append(group_list)
    return bool_list

def all_used(used):
    for letters_used in used:
        for l in letters_used:
            if not l:
                return False
    return True

def search(groups, solutions, solution, word, used, last_group_i, used_new_since_last_starting, subdict, max):
    #print("search " + str(solution) + " " + word + " " + str(used) + " " + str(last_group_i))
    for group_i in range(len(groups)):
        if group_i == last_group_i:
            continue
        for letter_i in range(len(groups[group_i])):
            letter = groups[group_i][letter_i]
            #print("try " + letter)
            if letter in subdict:
                next_used = [x[:] for x in used] #deep copy
                next_used_new_since_last_starting = used_new_since_last_starting
                if not next_used[group_i][letter_i]:
                    next_used_new_since_last_starting = create_bool_list(groups, True)
                next_used[group_i][letter_i] = True
                next_word = word + letter
                next_subdict = subdict[letter]
                if end in next_subdict:
                    #completes a word
                    if next_word not in solution:
                        new_solution = solution[:]
                        new_solution.append(next_word)
                        if all_used(next_used):
                            solutions.append(new_solution)
                            print("Found solution: " + str(new_solution))
                        else:
                            if len(new_solution) < max and next_used_new_since_last_starting[group_i][letter_i]: #should this be checking first letter of word and not current letter?
                                next_used_new_since_last_starting_2 = [x[:] for x in next_used_new_since_last_starting]
                                next_used_new_since_last_starting_2[group_i][letter_i] = False
                                #recurse starting new word with next letter
                                search(groups, solutions, new_solution, letter, next_used, group_i, next_used_new_since_last_starting_2, dictionary[letter], max)
                #recurse with next letter added
                search(groups, solutions, solution, next_word, next_used, group_i, next_used_new_since_last_starting, next_subdict, max)


def main():
    print("Building dictionary...")
    build_dictionary()
    print("Done!")

    groups_str = input("Enter letters in groups (ex: WHI ESD LAK BNO): ")
    groups = groups_str.split() #["WHI", "ESD", "LAK", "BNO"]
    
    no_letters_used = create_bool_list(groups, False)
    
    used_new_since_last_starting = create_bool_list(groups, False)
    
    print("Searching...")
    for max in range(1, max_words + 1):
        print("Searching for length " + str(max))
        solutions = []
        search(groups, solutions, [], "", no_letters_used, -1, used_new_since_last_starting, dictionary, max)
        if len(solutions) > 0:
            #search(groups, solutions, [], "SHA", [[False, True, False], [False, True, False], [False, True, False], [False, False, False]], -1, create_bool_list(groups, True), dictionary["S"]["H"]["A"])
            print(solutions)
            return


if __name__ == "__main__":
    main()