import numpy as np
import random
import time
from wordle import Solver, Wordle, load_vocab


def simulate(vocab, answers, n_simulations, guess_point):
    turns = np.zeros(n_simulations)
    answer_list = random.sample(answers, n_simulations)

    for i, answer in enumerate(answer_list):
        solver = Solver(vocab, answers, "TRACE", guess_point)
        wordle = Wordle(answer)
        turn = 0
        print(f"\nSIMULATION {i+1}")
        while True:
            turn += 1
            result = wordle.give_result(solver.word)
            print(f"    guess {turn}: {solver.word} = {result}")
            if result == "ggggg": break

            solver.filter_answers(result)
            solver.filter_vocab(result)
            solver.best_word()
        turns[i] = turn
    return np.mean(turns)



vocab, answers =load_vocab("guesses.txt", "solutions.txt")

start = time.time()

gps = [15, 18, 21, 24]
runs = []

for gp in gps:
    start = time.time()
    average = simulate(vocab, answers, 100, gp)
    duration = time.time() - start
    run = (gp, average, duration)
    runs.append(run)


for run in runs:
    print(f"\nguess point = {run[0]}")
    print(f"average # of turns = {run[1]}")
    print(f"time taken = {run[2]:.2f}")