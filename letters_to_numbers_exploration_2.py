# !/usr/bin/env python3

# https://stackoverflow.com/questions/6573415/evolutionary-algorithm-for-the-theo-jansen-walking-mechanism
# https://github.com/MorvanZhou/Evolutionary-Algorithm
# https://www.bing.com/search?q=evolutionary+algorithm+python&FORM=QSRE3
# http://www.ijcsit.com/docs/Volume%207/vol7issue2/ijcsit2016070212.pdf
# https://scanftree.com/tutorial/algorithms/backtracking/solving-cryptarithmetic-puzzles/
# https://www.geeksforgeeks.org/solving-cryptarithmetic-puzzles-backtracking-8/
# https://www.campusgate.co.in/2015/10/cryptarithmetic-solution-solved-examples.html
# www.theprojectspot.com/tutorial-post/creating-a-genetic-algorithm-for-beginners/3

# implementation of a genetic algorithm
# https://www.geeksforgeeks.org/genetic-algorithms/
# https://www.tutorialspoint.com/genetic_algorithms/
# https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_parent_selection.htm

#  MOST + MORE = TOKYO

import random
import copy


class Chromosome:

    pos = [0, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, words):
        self.a = words[0]
        self.b = words[1]
        self.c = words[2]

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

    def new_cr_from_old(self, chromosome):
        new_ex = chromosome[1:]
        random.shuffle(new_ex)
        new_ex = [1] + new_ex
        health = self.score(new_ex)
        return [health, new_ex, 0]


class Population(Chromosome):

    def __init__(self, args,
                 population_size,
                 number_of_children,
                 tournament_size):
        super().__init__(*args)
        self.population = population_size
        self.children = number_of_children
        self.k = tournament_size

    def parent_pop(self):
        for i in range(self.population):
            random.shuffle(self.pos)
            yield i, [1] + self.pos

    def new_parents_by_tournament(self, parents):
        """


        returns a list of winning parents, keys to self.parents
        """
        population = list(parents.keys())
        tournaments = len(population)
        new_parents = []
        for _ in range(tournaments):
            participants = random.sample(population, self.k)
            best_health = int("9" * len(self.c))
            winner = None
            for participant in participants:
                health_score = self.score(parents[participant][0])
                if abs(best_health) > abs(health_score):
                    best_health = health_score
                    winner = participant
                elif abs(best_health) == abs(health_score):
                    winner = random.sample([winner, participant], 1)[0]
            new_parents.append(winner)
        return new_parents

    def swap_positions(self):
        """
        Pick two random numbers, not equal, and return them.

        swap_pos_1: int
        swap_pos_2: int
        swap_pos_1 < intswap_pos_2
        swap_pos_1 and swap_pos_2 represents the index of chromosome positions
        return: list, [swap_pos_1, swap_pos_2]
        """
        swap_pos = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return sorted(random.sample(swap_pos, 2))

    def swap_mutation(self, chromosome):

        siblings = []
        for _ in range(self.children):
            child = copy.deepcopy(chromosome)

            swap_pos = self.swap_positions()
            pos1 = swap_pos[0]
            pos2 = swap_pos[1]

            temp = child[pos1]
            child[pos1] = child[pos2]
            child[pos2] = temp

            siblings.append(child)

        return siblings

    def scramble_mutation(self, chromosome):

        child = copy.deepcopy(chromosome)

        swap_pos = self.swap_positions()
        pos1 = swap_pos[0]
        pos2 = swap_pos[1]

        start_ch = chromosome[:pos1]
        finish_ch = chromosome[pos2:]
        scramble = chromosome[pos1:pos2]
        random.shuffle(scramble)
        child = start_ch + scramble + finish_ch

        return child

    def invertion_mutation(self, chromosome):

        child = copy.deepcopy(chromosome)

        swap_pos = self.swap_positions()
        pos1 = swap_pos[0]
        pos2 = swap_pos[1]

        start_ch = chromosome[:pos1]
        finish_ch = chromosome[pos2:]
        invert = chromosome[pos1:pos2]
        invert.reverse()
        child = start_ch + invert + finish_ch

        return child


class ExplorePopulation:
    def __init__(self, generations, args, kwargs):
        self.generations = generations
        self.current_gen = 1
        self.pop = Population(args, **kwargs)

        self.parents = {'G' + str(i + 1): [g, 0]
                        for i, g in self.pop.parent_pop()}

    def cycle_gen(self):
        """
        new_parents is a list of keys from self.parents dictionary.
        """
        right_chromosome = {}
        while self.current_gen <= self.generations:
            print(f"\ncurrent_gen: {self.current_gen}\n")
            new_parents = self.pop.new_parents_by_tournament(self.parents)
            explored = self.next_gen(new_parents)

            for ind in range(len(explored)):
                var = 5 * self.pop.children ** (1 / (3 * self.pop.children))

                all_info = explored[ind]
                health_score = all_info[0]
                chr = all_info[1]
                generation = all_info[2]
                if health_score == 0:
                    right_chromosome.update(
                        self.perfect_score_stat(right_chromosome, all_info))
                    explored[ind] = self.pop.new_cr_from_old(chr)
                    # explored[ind] = self.new_cr_from_old(chr)

                elif generation >= round(var):
                    print(f"round(var): {round(var)}")
                    explored[ind] = self.mutate_stale(chr)

            health_frequency = {}
            for ind in range(len(explored)):
                health = explored[ind][0]
                if health not in health_frequency:
                    health_frequency[health] = []
                health_frequency[health].append(ind)
            print(f"\nfrequencies: {len(health_frequency)}")
            for frequency, index_list in health_frequency.items():
                print(f"{frequency:8}: index_list: {str(index_list):>35},\
                {len(index_list):3}\
                magic number: {round(0.2 * self.pop.population): 3}  \
                {str(len(index_list) >= round(0.2 * self.pop.population)):>9}")
                if len(index_list) >= round(0.2 * self.pop.population):
                    start_ind = 2
                    if 0 < round(0.2 * self.pop.population) < 3:
                        start_ind = 1

                    for ind in index_list[start_ind:]:
                        chr = explored[ind][1]
                        new_explored_chromosome = self.pop.new_cr_from_old(chr)
                        # new_explored_chromosome = self.new_cr_from_old(chr)
                        explored[ind] = new_explored_chromosome
                        print(f"ind: {ind} for explored,\
                        new explored[ind]: {new_explored_chromosome}")

            for parent, nxt_gen in zip(self.parents.keys(), explored):
                if list(nxt_gen[1:]) != []:
                    pass
                else:
                    print(f"\n{self.current_gen}\
                    empty parent: {list(nxt_gen[1:])}, {list(nxt_gen)}\n")
                self.parents[parent] = list(nxt_gen[1:])

            self.current_gen += 1

        print()

        print(f"key: {self.pop.chromosome_key}")
        # find differnt chromosomes if not unique answer
        # find the set of child_cromosome_keys
        # find the words and their values
        # if right_chromosome:
        #     right_chromosome = right_chromosome.keys
        #     print(f"{self.pop.a}: {}")
        #     print(f"significant part of chromosome: {}")

        if not right_chromosome:
            print(f"No right_chromosome achieved.")

        for generation in right_chromosome:
            print(f"gen: {generation:4},\
                    chromosome: {right_chromosome[generation]}")
        return None

    def perfect_score_stat(self, right_chromosome, all_info):
        if self.current_gen in right_chromosome:
            value = right_chromosome[self.current_gen]
        else:
            value = []

        key = self.current_gen
        value.append(all_info)
        return {key: value}

    def check_health(self, explored):
        """
        health is a list of the best health score from each aprent and mutated
            children group. health scores ar integers
        """
        health = [sub_lst[0][0] for sub_lst in explored]

    def parent_and_children(self):
        random.shuffle(self.pop.pos)
        parent = [1] + self.pop.pos
        health = self.pop.score(parent)
        return [[health, parent, 0]]

    def mutate_stale(self, chromosome):
        mutation_method = [self.pop.scramble_mutation,
                           self.pop.invertion_mutation]
        random.shuffle(mutation_method)
        m = str(mutation_method[0]).split()[2]
        print(f"mutation_method[0]: {m}")
        mutated = mutation_method[0](chromosome)
        health = self.pop.score(mutated)
        return [health, mutated, 0]

    def next_gen(self, new_parents):
        """ only swap_mutatiomn
            possibilities list of lists, [[health, chromosome, generation]]
                sorted by health score
            self.parents[parent] is a list with chromosome and its generation
        """
        possibilities = []
        for parent in new_parents:
            best_chrs = []
            children = []
            parent_chr = copy.deepcopy(self.parents[parent][0])
            par_score = [self.pop.score(parent_chr)]
            [par_score.append(parent_info)
             for parent_info in self.parents[parent]]
            par_score[2] += 1
            best_chrs.append(par_score)
            # print(f"parent stat: {best_chrs}")
            children = self.pop.swap_mutation(parent_chr)
            chil_score = [[self.pop.score(child), child, 0]
                          for child in children]
            [best_chrs.append(child_info) for child_info in chil_score]
            best_chrs.sort(key=lambda lst: abs(lst[0]))
            best_chr = best_chrs[0]
            possibilities.append(best_chr)
        possibilities.sort(key=lambda lst: abs(lst[0]))
        print(f"len: {len(possibilities)}.  possibilities:")
        for pos in possibilities:
            print(f" {pos}")
        return possibilities


evolutions = 125
# number of individuals participating in tournament selection, greater numbers
# == > more squed towards faster convergence
kwargs = {
    "tournament_size": 2,
    "population_size": 20,
    "number_of_children": 3
}
cryptarithmetic_puzzle1 = ["SEND", "MORE", "MONEY"]
cryptarithmetic_puzzle2 = ["BASE", "BALL", "GAMES"]
cryptarithmetic_puzzle3 = ["ATTRACTIONS", "INTENTIONS", "REGENERATION"]
cryptarithmetic_puzzle4 = ["WEIN", "WEIB", "LIEBE"]
cryptarithmetic_puzzle5 = ["MOST", "MOST", "TOKYO"]
# KEY: MDENORSY, chromosome: 17560892 34 or 43
pop = ExplorePopulation(evolutions, [cryptarithmetic_puzzle2], kwargs)
pop.cycle_gen()
