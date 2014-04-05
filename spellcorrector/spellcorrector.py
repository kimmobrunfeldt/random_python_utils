

import Levenshtein
from fuzzyfind import find_best_match


def find_similar_word(word, words, max_diff=None):
    """Finds best match for word from words.
    max_diff: See find_best_match()."""
    func = lambda x, y: 1.0 - Levenshtein.ratio(x, y)
    return find_best_match(word, words, func, max_diff=max_diff)


def main():
    words = open('wordsEn.txt').read().splitlines()
    wordset = set(words)

    while True:
        word = raw_input('Write word: ').strip()
        if word in wordset:
            print('Word is correct.')
        else:
            print('Did you mean %s?' % find_similar_word(word, words))


if __name__ == '__main__':
    main()
