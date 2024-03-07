Python Wordle solver.

play.py takes prompts user to play a word and then takes the result as user input.

simulate.py solves a simulated game of wordle without user interation in order to test for the optimal guess_point hyperparameter.

wordle.py contains the Wordle and Solver classes.


Wordle class is initialized with the answer and has a single class method give_result to return a result from an input word guess.


Solver class:

- The filter_answers and filter_vocab class methods remove words from the set of possible answers and the set of all legal words (full wordle vocabulary) respectively. Guesses are initally selected from the full vocabulary in order to not be constrained to guessing words that are possible solutions, which is rarely optimal (and actually Wordle "hard mode"). Once the number of possible solutions (size of the set of possible answers) reaches a certain number (determined by the guess_point hyperparameter), guesses are made from the answer set.

- The best word to guess next is determined by the best_word class method based on the word with the lowest score, as detemined by the word_score class method. A score is given to each word in whichever word set is currently in use. For a given word, the set of possible answers is filtered using every possible result it might recieve in turn, and the average over these resulting sizes is the score (lowest score is best). The next word chosen is therefore the word that reduces the answer set the most on average.

- The scoring method is time-intensive, but reduces drastically with a smaller vocabulary. We therefore pre-determine the best choice of first word when the vocab has not yet been reduced, as this is constant over games anyway.