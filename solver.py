import random
import sys

solutions = open("solutions.txt", "r")
helpers = open("helpers.txt", "r")
counts = open("extension/words/word_counts.txt", "r")

allSolutions = solutions.read().split("\n")
allHelpers = helpers.read().split("\n")
allHelpers = list(filter(lambda x: allHelpers.index(x) % 10 == 0, allHelpers))
freqCounts = counts.read().split("\n")

solutions.close()
helpers.close()
counts.close()


class Dict(dict):
        def __missing__(self, key):
            return 0


allCounts = {0:Dict(), 1:Dict(), 2:Dict(), 3:Dict(), 4:Dict(), 5:Dict()}
for count in freqCounts:
    count = count.split(",")

    allCounts[int(count[0])][count[1]] = int(count[2])


def getGuess(validSolutions, validHelpers):

    maxScore = 0
    bestWord = validSolutions[0]

    for candidate in validSolutions:
        score = 0

        for i in range(len(candidate)):
            score += allCounts[i][candidate[i]]

        if score > maxScore:
            maxScore = score
            bestWord = candidate

    return bestWord


def getGuessDynamically(validSolutions, validHelpers):

    if len(validSolutions) == len(allSolutions):
        return "soare"

    maxScore = 0
    bestWord = validSolutions[0]

    for candidate in validSolutions + validHelpers:
        score = 0

        for other in validSolutions:
            score += markGuess(other, candidate)[1]
        
        if score > maxScore:
            maxScore = score
            bestWord = candidate

    print(bestWord, score)
    return bestWord


def getGuessFrequency(validSolutions, validHelpers):

    maxScore = 0
    bestWord = validSolutions[0]

    for candidate in validSolutions:
        score = 0

        for count in freqCounts:
            count = count.split(" ")

            if count[0] in candidate:
                score += int(count[1])
        
        if score > maxScore:
            maxScore = score
            bestWord = candidate

    return bestWord


def getGuessRandom(validSolutions, validHelpers):
    return random.choice(validSolutions)


def markGuess(answer, guess):
    res = [list(t) for t in zip(answer, guess, "NNNNN")]
    score = 0

    for r in res:
        if r[0] == r[1]:
            r[2] = "C"
            score += 5
    
    for r in res:
        if r[2] != "C" and r[1] in answer and answer.count(r[1]) > sum([1 if n != "N" and g == r[1] else 0 for _, g, n in res ]):
            r[2] = "P"
            score += 2
    
    return res, score


def pruneSearchSpace(res, validSolutions, validHelpers):

    counts = Dict()
    i = 0
    for _, g, r in res:
        if r == "C":
            validSolutions = list(filter(lambda sol: sol[i] == g, validSolutions))
            validHelpers = list(filter(lambda sol: sol[i] == g, validHelpers))
        else:
            validSolutions = list(filter(lambda sol: sol[i] != g, validSolutions))
            validHelpers = list(filter(lambda sol: sol[i] != g, validHelpers))

        if r != "N":
            counts[g] += 1

        i += 1

    for letter, count in counts.items():
        validSolutions = list(filter(lambda sol: sol.count(letter) >= count, validSolutions))
        validHelpers = list(filter(lambda sol: sol.count(letter) >= count, validHelpers))

    print(len(validSolutions), len(validHelpers))
    return validSolutions, validHelpers


def solveFor(answer):
    validSolutions = list(allSolutions)
    validHelpers = list(allHelpers)

    tries = 0

    res = []
    while len(res) == 0 or not all(r == "C" for _, _, r in res):
        guess = getGuess(validSolutions, validHelpers)
        res, _ = markGuess(answer, guess)
        validSolutions, validHelpers = pruneSearchSpace(res, validSolutions, validHelpers)
        tries += 1

    print(answer, tries)
    return tries


def scoreAlg():
    scores = []
    for word in allSolutions:
        scores.append(solveFor(word))

    print("avg: %.2f, min: %.2f, max: %.2f" % (sum(scores) / len(scores), min(scores), max(scores)))

scoreAlg()
# random: avg: 4.91, min: 2.00, max: 13.00
# using most information on 1 letter: avg: 6.22, min: 1.00, max: 14.00
# using most information on 2 letters: avg: 5.01, min: 1.00, max: 10.00
# using most frequent on 1 letter: avg: 4.65, min: 1.00, max: 11.00
# using most frequent on 2 letters: avg: 4.64, min: 1.00, max: 11.00
# using most frequent on 3 letters: avg: 4.64, min: 1.00, max: 11.00
# using most frequent on 3 letters weighted: avg: 4.37, min: 1.00, max: 11.00
# using most frequent on trigram only: avg: 4.15, min: 1.00, max: 9.00
# using most frequent on bigram and trigram only: avg: 4.15, min: 1.00, max: 9.00
# calculating best word dynamically: avg: 3.31, min: 1.00, max: 6.00
# calculating best word dynamically full table: avg: 3.23, min: 2.00, max: 7.00
# calculating best word freq per letter: avg: 3.57, min: 1.00, max: 7.00
# calculating best word freq per letter with helpers: avg: 4.23, min: 2.00, max: 9.00
# calculating best word freq per letter full set: avg: 4.63, min: 1.00, max: 12.00
# calculating best word freq per letter with vowel priority full set: avg: 4.80, min: 1.00, max: 12.0
# most information word freq per letter min small set: avg: 3.82, min: 1.00, max: 9.00
# most information word freq per letter max small set: avg: 3.57, min: 1.00, max: 7.00
# random small set: avg: 3.76, min: 2.00, max: 9.00
# most information word freq per letter max small set with helpers: avg: 4.23, min: 2.00, max: 9.00
# most information word freq per letter max small set with total freq: avg: 3.77, min: 1.00, max: 9.00
# most information word freq per letter max small set with total freq weighted: avg: 3.53, min: 1.00, max: 7.00
# most information word freq per letter max small set with total freq weighted and randomness: avg: 3.57, min: 1.00, max: 8.00
