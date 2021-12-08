import utils

SYMBOL_PATTERNS = ('ABCEFG', 'CF', 'ACDEG', 'ACDFG', 'BCDF', 'ABDFG', 'ABDEFG', 'ACF', 'ABCDEFG', 'ABCDFG')
LETTERS = ('C', 'F', 'A', 'B', 'D', 'E', 'G')  # orders from the shortest patterns, a bit more effective


def main():
    lines = utils.read_strings('inputs/day_08.txt')

    unique_digits = {1, 4, 7, 8}
    unique_digit_count = 0
    result_sum = 0
    for line in lines:
        parts = line.split(' | ')
        decoder = Decoder(parts[0].split(' '))
        decoded_result = decoder.decode(parts[1].split(' '))
        result_number = 0
        for digit in decoded_result:
            if digit in unique_digits:
                unique_digit_count += 1
            result_number = result_number * 10 + digit
        result_sum += result_number

    print(f'Digits {unique_digits} appear {unique_digit_count} times in the output')
    print(f'Sum of all the output values: {result_sum}')


class Decoder:
    def __init__(self, patterns):
        # sort patterns according to their length (shorter patterns will match faster)
        self.patterns = patterns
        self.patterns.sort(key=lambda s: len(s))

        # sort letters so that first are the letters from the shortest patterns (wrong mappings are identified much sooner that way)
        self.letters = self.sort_letters()

    def sort_letters(self):
        remaining_letters = set(LETTERS)
        sorted_letters = []
        for pattern in self.patterns:
            for letter in pattern:
                if letter.upper() in remaining_letters:
                    sorted_letters.append(letter)
                    remaining_letters.remove(letter.upper())
                    if len(remaining_letters) == 0:
                        return sorted_letters  # all letters placed

    def decode(self, symbols_encoded):
        mapping = self.find_mapping(0, self.patterns)

        result = [0] * len(symbols_encoded)
        for i, encoded in enumerate(symbols_encoded):
            decoded = encoded
            for key in mapping:
                decoded = decoded.replace(key, mapping[key])
            result[i] = SYMBOL_PATTERNS.index(''.join(sorted(decoded)))

        return result

    # all pattern (original) letters are lowercase (self.letters, self.patterns)
    # all symbol (replacement) letters are uppercase (LETTERS, SYMBOL_PATTERNS)
    def find_mapping(self, depth, patterns):
        letter = self.letters[depth]  # choose the current letter according to the internal letter ordering
        for new_letter in LETTERS:
            # replace letter with new_letter in patterns and try to match against the symbols
            patterns_replaced = [p.replace(letter, new_letter) for p in patterns]
            fully_replaced, partially_replaced = [], []
            for p in patterns_replaced:
                fully_replaced.append(p) if p.upper() == p else partially_replaced.append(p)
            if not match_symbols(fully_replaced):
                continue  # this replacement is not possible, try next one

            # if in last level, return the single-letter mapping
            if depth == (len(LETTERS) - 1):
                return {letter: new_letter}

            # if not, go to next level of recursion and join
            child_mapping = self.find_mapping(depth + 1, partially_replaced)  # fully replaced patterns do not matter in lower levels
            if child_mapping != {}:
                return {**{letter: new_letter}, **child_mapping}  # append dicts

        return {}  # tried all substitutes, none is possible -> fail and go up


def match_symbols(patterns):
    for pattern in patterns:
        sorted_pattern = ''.join(sorted(pattern))
        if sorted_pattern not in SYMBOL_PATTERNS:
            return False  # this patten does not match any symbol
    return True  # every pattern matches at leas one symbol


if __name__ == '__main__':
    main()
