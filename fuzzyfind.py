"""
Problem:
    You have a list of 'real' words. Then you have a list of all words
    which may contain similar words than the real words.
    For all words in all_words, find the best match from real_words.
Example:
    real_words = ['apple', 'grape', 'pineapple']
    all_words = ['apple1', 'apple', 'greip', 'greb', 'grape',
                 'grabe', 'painapple', 'pinaple', 'pineapple']

    find_similar_words(real_words, all_words) should return:

    {
     'apple': 'apple', 'apple1': 'apple',
     'greip': 'grape', 'greb': 'grape', 'grape': 'grape', 'grabe': 'grape',
     'painapple': 'pineapple', 'pinaple': 'pineapple', 'pineapple': 'pineapple'
    }

     Or similar format which tells the same information.
"""


import difflib


def find_best_match(item, seq, diff_func, max_diff=None):
    """Finds best match for item 'item' from iterable 'seq'.
    diff_func: Function that compares the difference between two items,
               it must return int/float. The smaller the number,
               the more similar items are.
    max_diff: Optional number value. If the best found match differs from the
              actual item more than this value(diff_func(a, b) > max_diff),
              None is returned. Meaning that none of the items in 'seq'
              is close enough.

    Returns the item from 'seq' which had highest match.
    """
    # Calculate similarity ratios for all words.
    similarity_ratios = []

    for s in seq:
        ratio = diff_func(item, s)
        similarity_ratios.append((ratio, s))

    # Finds the real word which has the biggest similarity ratio
    best_match = min(similarity_ratios, key=lambda x: x[0])

    if max_diff is not None and best_match[0] > max_diff:
        return None

    return best_match[1]


def find_similar_word(word, words, max_diff=None):
    """Finds best match for word from words.
    max_diff: See find_best_match()."""
    # Use difflib's SequenceMatcher as the diff_func.
    # "As a rule of thumb, a ratio() value over 0.6 means the sequences
    # are close matches". Therefore max_diff=0.4 would find close matches.
    func = lambda x, y: 1.0 - difflib.SequenceMatcher(None, x, y).ratio()
    return find_best_match(word, words, func, max_diff=max_diff)


def find_similar_words(real_words, all_words, max_diff=None):
    """For all words in all_words, finds the best match from real_words.
    max_diff: See find_best_match().
    Returns 'many-to-one' dictionary. It is guaranteed that returned dictionary
    contains all words that are in all_words. You can access the best found
    match with k[word_from_all_words].
    """
    k = {}
    for word in all_words:
        best_match = find_similar_word(word, real_words, max_diff=max_diff)
        k[word] = best_match

    return k


def find_closest_number(number, numbers):
    func = lambda x, y: abs(x - y)
    return find_best_match(number, numbers, func)


def find_closest_numbers(numbers, all_numbers):
    k = {}
    for number in all_numbers:
        best_match = find_closest_number(number, numbers)
        k[number] = best_match

    return k


def main():
    real_words = ['apple', 'grape', 'pineapple']
    all_words = ['apple1', 'apple', 'greip', 'greb', 'grape',
                 'grabe', 'painapple', 'pinaple', 'pineapple']

    best_match = find_similar_word('appl', real_words)
    print('Best match for \'appl\' is \'%s\'\n' % best_match)

    print('All similar words:')
    print(find_similar_words(real_words, all_words))

    print('\nAll similar words with max_diff specified:')
    print(find_similar_words(real_words, all_words, max_diff=0.3))

    numbers = [1, 3, 10, 40, 100]
    all_numbers = [1, 1.93, 2.1, 2, 4, 6, 50, 150, 2000]
    print('\nAll close numbers:')
    print(find_closest_numbers(numbers, all_numbers))


if __name__ == '__main__':
    main()
