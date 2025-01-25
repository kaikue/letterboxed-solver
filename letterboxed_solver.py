#at least 3 letters long
#can reuse letters
# consecutive letters not from same side
# last letter of word = first letter of next word

# use all letters
# find fewest words
#   find shortest words

# input: 4 groups of 3 letters: WHI ESD LAK BNO (order doesn't matter)
# construct trie (just once!)
# DFS
# for each letter:
#   for each letter on other sides (unused first?)
#       add that letter to used set
#       if completes a word:
#           if word was already played: return fail
#           if all letters used: return success
#           else: recurse starting new word with that letter
#           (keep going to next in case of subword e.g. COUNTER/COUNTERPART)
#       if valid options with that letter added:
#           recurse with that letter added
#       else: return fail
# look at all successes, select fewest words then shortest total words length

dictionary = {}
end = None
max_words = 5

def build_dictionary():
    words_file = open("words_alpha_len3plus.txt", "r")
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

def search(groups, solutions, solution, word, used, last_group_i, used_new_since_last_starting, subdict):
    #print("search " + str(solution) + " " + word + " " + str(used) + " " + str(last_group))
    for group_i in range(len(groups)):
        if group_i == last_group_i:
            continue
        for letter_i in range(len(groups[group_i])):
            letter = groups[group_i][letter_i]
            #print("try " + letter)
            if letter not in subdict:
                return False
            next_used = [x[:] for x in used] #deep copy
            #keep track of letters started at without used update- returning to one of them should be a fail?
            #if you finish a word and return to a previously used starting letter while using no new letters since starting with that, then fail (what if its a shorter path? o well it's a bad circuitous route anyway)
            #used_at_last_start[group_i][letter_i]
            #set at word start
            #check at word end
            next_used_new_since_last_starting = used_new_since_last_starting
            if not next_used[group_i][letter_i]:
                next_used_new_since_last_starting = create_bool_list(groups, True)
            next_used[group_i][letter_i] = True
            next_word = word + letter
            next_subdict = subdict[letter]
            if end in next_subdict:
                #completes a word
                if next_word in solution:
                    return #duplicate word- fail
                new_solution = solution[:]
                new_solution.append(next_word)
                if all_used(next_used):
                    solutions.append(new_solution)
                    print("Found solution: " + str(new_solution))
                    return #success
                else:
                    if len(new_solution) >= max_words:
                        return #solution would get too long
                    if not next_used_new_since_last_starting[group_i][letter_i]:
                        return #back at an old starting letter and haven't used any new letters since we last started there
                    next_used_new_since_last_starting_2 = [x[:] for x in next_used_new_since_last_starting]
                    next_used_new_since_last_starting_2[group_i][letter_i] = False
                    #recurse starting new word with next letter
                    search(groups, solutions, new_solution, letter, next_used, group_i, next_used_new_since_last_starting_2, dictionary[letter])
            #recurse with next letter added
            search(groups, solutions, solution, next_word, next_used, group_i, next_used_new_since_last_starting, next_subdict)


def main():
    print("Building dictionary...")
    build_dictionary()
    print("Done!")
    #print(dictionary["a"]["r"]["i"]["s"])

    groups_str = input("Enter letters in groups (ex: WHI ESD LAK BNO): ")
    groups = groups_str.split() #["WHI", "ESD", "LAK", "BNO"]
    
    no_letters_used = create_bool_list(groups, False)
    
    """
    used_when_last_starting = []
    for group_i in range(len(groups)):
        group_used_when_last_starting = []
        for _ in range(len(groups[group_i])):
            group_used_when_last_starting.append(no_letters_used)
        used_when_last_starting.append(group_used_when_last_starting)
    """
    used_new_since_last_starting = [x[:] for x in no_letters_used]
    
    print("Searching...")
    solutions = []
    search(groups, solutions, [], "", no_letters_used, -1, used_new_since_last_starting, dictionary)
    print(solutions)


if __name__ == "__main__":
    main()