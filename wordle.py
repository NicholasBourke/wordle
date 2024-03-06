import numpy as np
import io


class Solver:
    def __init__(self, vocab, answers, init_word, guess_point=20):
        self.vocab = vocab
        self.answers = answers
        self.n_words = len(vocab)
        self.n_answers = len(answers)
        self.word = init_word
        self.guess_point = guess_point

    def filter_answers(self, result, mode="filter", score_word=""):
        """
        Filters out incorrect answers based on the result of the last word.
        Also used to score words to determine optimal next word choice.
        """
        answers = self.answers
        green_yellow = []
        black = []

        if mode == "filter":
            filter_word = self.word
        if mode == "score":
            filter_word = score_word

        # POSITIONAL FILTERING
        for k, colour in enumerate(result):
            letter = filter_word[k]
            # filter out words that don't match green letters in result
            if colour == "g":
                answers = [word for word in answers if word[k] == letter]
                green_yellow.append(letter)
            # filter out words that match yellow letters in result
            if colour == "y":
                answers = [word for word in answers if word[k] != letter]
                green_yellow.append(letter)
            # filter out words that match black letters in result
            if colour == "b":
                answers = [word for word in answers if word[k] != letter]
                black.append(letter)

        # LETTER COUNT FILTERING
        for letter in black:
            n = green_yellow.count(letter)  # count occurences of "letter"
            # filter out words without n occurences
            answers = [word for word in answers if word.count(letter) == n]

        # YELLOW FILTERING
        # consider remaining yellow letters (note: and green, but inconsequential)
        green_yellow = [letter for letter in green_yellow if letter not in black]
        for letter in green_yellow:
            # filter out words that don't contain all yellow letters somewhere
            answers = [word for word in answers if letter in word]

        if mode == "filter":
            self.answers = answers
            self.n_answers = len(answers)
        if mode == "score":
            return len(answers)

    def filter_vocab(self, result):
        """
        Filters out words from the vocabulary from which a next word is chosen.
        Not necessary for accuracy but improves runtime dramatically.
        Aim is to filter out words which are clearly not optimal,
        eg. with yellows/blacks in same position.
        Possible that words with greens in same position should be filtered, but
        retained here to allow for possibility of correct solution at every word.
        Probably a mistake to over-filter here as speed gains are sufficient as is.
        """
        green_yellow = []
        black = []

        # POSITIONAL FILTERING
        for k, colour in enumerate(result):
            letter = self.word[k]
            if colour == "g":
                green_yellow.append(letter)
            if colour == "y":
                self.vocab = [word for word in self.vocab if word[k] != letter]
                green_yellow.append(letter)
            if colour == "b":
                self.vocab = [word for word in self.vocab if word[k] != letter]
                black.append(letter)

        # LETTER COUNT FILTERING
        for letter in black:
            n = green_yellow.count(letter)
            self.vocab = [word for word in self.vocab if word.count(letter) <= n]

        self.n_words = len(self.vocab)
    
    def word_score(self, word):
        codes = ["b", "y", "g"]
        scores = []
        for cd1 in codes:
            for cd2 in codes:
                for cd3 in codes:
                    for cd4 in codes:
                        for cd5 in codes:
                            result = cd1 + cd2 + cd3 + cd4 + cd5
                            score = self.filter_answers(result, mode="score", score_word=word)
                            if score > 0:
                                scores.append(score)
        word_score = np.mean(np.array(scores))
        return word_score

    def best_word(self, print_progress=True):
        best_score = self.n_words
        best_word = ""

        # begin by choosing next word from full vocabulary to allow for optimal choices
        # once set of answers is small enough, choose from there to attempt solution
        if self.n_answers <= self.guess_point:
            words = self.answers
            print_progress = False
        else:
            words = self.vocab

        num_words = len(words)
        print_5 = int(num_words/20)

        for i, word in enumerate(words):
            word_score = self.word_score(word)
            if word_score < best_score:
                best_score = word_score
                best_word = word
            if print_progress and i % print_5 == 0:
                print(f"{int(i/num_words*100)}%:   best word: {best_word}, score = {best_score:.2f}")
        self.word = best_word



class Wordle:
    def __init__(self, answer):
        self.answer = answer

    def give_result(self, guess):
        result = ["b", "b", "b", "b", "b"]
        a = [*self.answer]
        for k, letter in enumerate(guess):
            if letter == self.answer[k]:
                result[k] = "g"
                a[k] = None
                guess = guess[:k] + "-" + guess[k+1:]
        for k, letter in enumerate(guess):
            if letter in a:
                result[k] = "y"
                a.remove(letter)
        return "".join(result)



def load_vocab(guess_path, answer_path):
    guesses = io.open(guess_path, encoding='utf-8').read().upper().split("\n")
    answers = io.open(answer_path, encoding='utf-8').read().upper().split("\n")
    full_vocab = answers + guesses
    return full_vocab, answers


