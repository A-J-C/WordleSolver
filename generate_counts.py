from collections import Counter

knuth = open("words/knuth.txt", "r")
output = open("words/word_counts.txt", "w")

knuth_contents = knuth.read()
words = knuth_contents.split("\n")

counter = Counter("".join(words))

for word in words:
    counter.update(map(''.join, zip(word, word[1:])))
    counter.update(map(''.join, zip(word, word[1:], word[2:])))
    counter.update(map(''.join, zip(word, word[1:], word[2:], word[3:])))

filtered_count = list(filter(lambda x: x[1] >= 10, counter.most_common()))
for gram, count in filtered_count:
    output.write(gram + " " + str(count) + "\n")

knuth.close()
output.close()