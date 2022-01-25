from collections import Counter

solutions = open("solutions.txt", "r")
output = open("extension/words/word_counts.txt", "w")

solution_contents = solutions.read()
words = solution_contents.split("\n")

for i in range(len(words[0])):
    counter = Counter([w[i] for w in words])
    for gram, count in counter.items():
        output.write(str(i) + "," + gram + "," + str(count) + "\n")

counter = Counter("".join(words))
for gram, count in counter.items():
    output.write("5," + gram + "," + str(count) + "\n")

solutions.close()
output.close()