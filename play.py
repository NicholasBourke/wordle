from wordle import Solver, load_vocab


vocab, answers =load_vocab("guesses.txt", "solutions.txt")

solver = Solver(vocab, answers, "TRACE")


while True:
    # display word to attempt
    print(f"\nPlease try {solver.word}")

    # take result as input
    result = input("Using g, y, b, enter result here: ")
    if result == "ggggg":
        print("DONE")
        break

    # filter answer and vocab sets
    solver.filter_answers(result)
    solver.filter_vocab(result)
    print(f"{solver.n_words} words remaining")
    print(f"{solver.n_answers} possible answers remaining")

    # determine next word with function
    solver.best_word()


    