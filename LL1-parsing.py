import sys

def first_char(non_terminals, grammar, key):
    first = set()
    for word in grammar[key]:
        if word[0] in non_terminals:
            first.update(first_char(non_terminals, grammar, word[0]))
        else:
            first.update(word[0])
    
    return first

def follow_set(non_terminals, grammar, first):
    follow = {}
    for i in non_terminals:
        follow[i] = set()
    follow[non_terminals[0]].add("$")
    
    flag = 2
    while flag:
        temp = follow.copy()
        flag = flag-1
        for i in grammar:
            for word in grammar[i]:
                for j in range(len(word)):
                    if word[j] in non_terminals:
                        if j+1 < len(word):
                            if word[j+1] in non_terminals:
                                follow[word[j]].update(first[word[j+1]])
                                if "ε" in first[word[j+1]]:
                                    follow[word[j]].update(follow[i])
                            else:
                                follow[word[j]].add(word[j+1])
                        else:
                            follow[word[j]].update(follow[i])
                        if temp != follow:
                            flag = 2
        follow[i].discard("ε")
    return follow
                    
def first_set(non_terminals, grammar):
    first = {}
    for i in non_terminals:
        temp = first_char(non_terminals, grammar, i)
        first[i] = temp

    return first

def firstable(grammar, non_terminals, terminals, key, target):
    for word in grammar[key]:
        if word[0] == target:
            return word
        elif word[0] in non_terminals:
            if firstable(grammar, non_terminals, terminals, word[0], target):
                return word
            else:
                return False

def ll1(non_terminals, terminals, grammar, first, follow):
    table = {}
    for i in non_terminals:
        table[i] = {}
        for j in terminals:
            table[i][j] = []
            
    for i in non_terminals:
        for j in first[i]:
            if (j == "ε"):
                continue
            word = firstable(grammar, non_terminals, terminals, i, j)
            if word!=False:
                table[i][j].append(word)
        if "ε" in first[i]:
            for j in follow[i]:
                table[i][j].append("ε")
    return table
            

# Main
# Only accepts non ambiguous grammar

n = int(input("Enter the number of grammar: "))

grammar = {}
non_terminals = []
terminals = set()

for i in range(n):
    key = input("Enter the key: ").strip()
    non_terminals.append(key)
    
    words = input("Enter the words: ").split("|")
    
    for j in range(len(words)):
        words[j] = words[j].strip()
        for k in words[j]:
            if k not in non_terminals:
                terminals.add(k)
        
    grammar[key] = words
    
terminals.discard("ε")
terminals.add("$")
    
first = first_set(non_terminals, grammar)
follow = follow_set(non_terminals, grammar, first)
table = ll1(non_terminals, terminals, grammar, first, follow)

for i in non_terminals:
    print("First(", i, "):", first[i])
for i in non_terminals:
    print("Follow(", i, "):", follow[i])

print("M[N,T]", end="\t")
for i in terminals:
    print(i, end="\t")
for i in non_terminals:
    print("\n\n", i, end="\t", sep="")
    for j in terminals:
        print(table[i][j], end="\t")
    print()