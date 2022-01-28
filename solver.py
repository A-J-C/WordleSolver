from collections import Counter
import random

solutions = open("solutions.txt", "r")
helpers = open("helpers.txt", "r")
#counts = open("extension/words/word_counts.txt", "r")

allSolutions = solutions.read().split("\n")
allHelpers = helpers.read().split("\n")
allHelpers = list(filter(lambda x: allHelpers.index(x) % 10 == 0, allHelpers))
#freqCounts = counts.read().split("\n")

solutions.close()
helpers.close()
#counts.close()


class Dict(dict):
        def __missing__(self, key):
            return 0


def getGuess(validSolutions, validHelpers):

    allCounts = {}
    for i in range(len(validSolutions[0])):
        allCounts[i] = Dict()
        counter = Counter([w[i] for w in validSolutions])
        for gram, count in counter.items():
            allCounts[i][gram] = count

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
    potentialNots = []
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
        else:
            potentialNots += [g]  

        i += 1

    for letter, count in counts.items():
        validSolutions = list(filter(lambda sol: sol.count(letter) >= count, validSolutions))
        validHelpers = list(filter(lambda sol: sol.count(letter) >= count, validHelpers))

    for pot in potentialNots:
        if pot not in counts:
            validSolutions = list(filter(lambda sol: pot not in sol, validSolutions))
            validHelpers = list(filter(lambda sol: pot not in sol, validHelpers))

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