'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Returns the cosine similarity between vec1 and vec2
    vec1, vec2 -- dictionaries'''
    topvalue = 0
    botval1 = 0
    botval2 = 0
    check = 0


    botval1 = norm(vec1)
    botval2 = norm(vec2)

    for i, j in vec1.items():
        for x, y in vec2.items():
            if i == x:
                topvalue += (j*y)

    cos_sim = topvalue/(botval1 * botval2)
    return cos_sim




def build_semantic_descriptors(sentences): # THis function has the issues (please help :(
    d = {}
    w = {}
    in_sen = []

    for sen in sentences:
        sen = set(sen)
        sen = list(sen)

        for word1 in sen:
            if word1 in d:
                w = d[word1]

            for word2 in sen:
                if word2 != word1 and word1 != '' and word2 != '':
                    if word2 not in w:
                        w[word2] = 1
                    elif word1 in d and word2 in w:
                        w[word2] += 1

            d[word1] = w
            w = {}

    return d



def build_semantic_descriptors_from_files(filenames):

    combined_d = {}
    replace_pun = [",", "-", "--", ":", ";"]
    list_list = []

    for x in range(len(filenames)):
        file = open(filenames[x], encoding="utf-8").read()
        file = file.lower()

        for pun in replace_pun:
            file = file.replace(pun," ")

        file = file.replace("!",".").replace("?",".").replace(". ",".").replace("\n"," ")
        file = file.split(".")

        for string in file:
            check = string.split(" ")
            list_list.append(check)

        temp = build_semantic_descriptors(list_list)


        for key in temp:
            if key in combined_d:
                for val in combined_d[key]:
                    if val in temp[key]:
                        add_d = combined_d[key]
                        temp_add = temp[key]
                        temp_add[val] += add_d[val]
                    else:
                        add_d = combined_d[key]
                        temp[key][val] = add_d[val]

        combined_d.update(temp)
        list_list = []


    return combined_d


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_sim = -2
    max_choice = ""


    for x in range(len(choices)):
        if word in semantic_descriptors:
            word_d = semantic_descriptors[word]

            if choices[x] in semantic_descriptors:
                value = semantic_descriptors[choices[x]]

                local_max = similarity_fn(word_d, value)

            else:
                local_max = -1

        else:
            local_max = -1


        if local_max > max_sim:
            max_sim = local_max
            max_choice = choices[x]
        local_max = 0

    return max_choice




def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    total_flt = 0
    list_list = []

    file = open(filename).read()
    file = file.split("\n")

    for string in file:
        check = string.split(" ")
        list_list.append(check)


    for ln in list_list:
        if len(ln) > 2:
            test = most_similar_word(ln[0],ln[2:], semantic_descriptors, similarity_fn)
            if test == ln[1]:
                total_flt += 1

    return ((total_flt / len(file) ) * 100)


if __name__ == '__main__':

    sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")





