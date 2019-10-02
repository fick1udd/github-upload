# !/usr/bin/env python3

from itertools import permutations


class Chromosome:

    pos = [0, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        self.chromosome_key = self.char_set()

    def char_set(self):
        temp_comb1 = set(self.a + self.b + self.c)
        temp_comb2 = list(temp_comb1)

        first_char_in_c = self.c[0]
        temp_comb2.remove(first_char_in_c)

        temp_comb2.sort()

        temp_comb2 = [first_char_in_c] + temp_comb2

        comb = ''.join(temp_comb2)
        return comb

    def word_amount(self, word, chromosome):
        sum = ""
        for char in word:
            indx = self.chromosome_key.index(char)
            sum += str(chromosome[indx])
        return sum

    def score(self, chromosome):
        amounts = ["", "", ""]

        for i, word in zip(range(3), [self.a, self.b, self.c]):
            sum = self.word_amount(word, chromosome)
            amounts[i] = sum

        return int(amounts[2]) - (int(amounts[0]) + int(amounts[1]))


def ncs(nc):
    nc1 = [1] + [nc[0]] + [5, 6] + nc[1:]
    ind = nc.index(4)
    nc[ind] = 6
    nc2 = [1] + [nc[0]] + [4, 5] + nc[1:]
    return nc1, nc2


def run_perm2(perm):
    health_score = {}
    for p in perm:
        chs = ncs(list(p))

        ch1 = chs[0]
        ch2 = chs[1]

        score1 = a.score(ch1)
        score2 = a.score(ch2)
        diff = score1 - score2

        if diff not in health_score:
            health_score[diff] = []
        health_score[diff].append([score1, score2, ch1, ch2])

    for diff in health_score:
        health_score[diff].sort(key=lambda lst: lst[0])

    return health_score


def run_perm1(perm):
    health_score = {}
    p_lst = []
    for p in perm:
        p_lst.append(p)
        ch1 = [1] + list(p)

        score1 = a.score(ch1)

        if score1 not in health_score:
            health_score[score1] = []
        health_score[score1].append([score1, ch1])

    for score1 in health_score:
        health_score[score1].sort(key=lambda lst: lst[0])

    return health_score, p_lst

#     for diff in sorted(health_score):
#         print(f"\nFor diff {diff} there are {len(health_score[diff]) records}")
#         for s in health_score[diff]:
#             print(f"{s[2]}\n{s[3]}   {s[0]} - {s[1]} = {diff}\n")


words1 = {"a": "SEND", "b": "MORE", "c": "MONEY"}
words2 = {"a": "BASE", "b": "BALL", "c": "GAMES"}
a = Chromosome(**words2)
print(a.chromosome_key)
significant = len(a.chromosome_key) - 2

# chr1 = [1, 7, 5, 6, 0, 8, 9, 2, 3, 4]  # is the right chromosome, 4. 3]
#    also right.
# chr2 = [1, 7, 4, 5, 0, 8, 9, 2, 3, 6]  # generates a health score of 1 but
#   also -1, -3, -319, -1801, 1999

m_lst = [0, 2, 3, 4, 7, 8, 9]
pos = [0, 2, 3, 4, 5, 6, 7, 8, 9]
perm = permutations(m_lst)

# res = run_perm2(perm)
all_res1 = run_perm1(permutations(pos))
res = all_res1[0]
perms = all_res1[1]


print(f"perms: {len(perms)},   len(res): {len(res)}")
print(f"res[0]: {res[0]}")
counter = 1
for r in sorted(res):
    if len(res[r]) > 1:
        content = res[r]
        nl = []
        for c in content:
            nl.append(str(c[1][:-2]))
        nl = set(nl)
        print(f"count: {counter},  len(nl): {len(nl)}, r: {r}, set(res[r]): {nl}")
        counter += 1
# print(type(res), res)

# for r in res:
#     n = len(res[r])
#     print(f"{r}  {n}")
