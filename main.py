from collections import defaultdict
import numpy as np
from scipy import stats
from game import play_game
from game import SameColumnStrategy, DifferentColumnsStrategy, HybridStrategy


def monte_carlo_simulation(num_games, strategy, verbose):
    scores = []
    for _ in range(num_games):
        scores.append(play_game(strategy, verbose))
    return scores


def run_simulations(num_games, strategies, verbose):
    results = {}
    for strategy_name, strategy_class in strategies.items():
        print(
            f"\nRunning simulation for strategy: {strategy_name.replace('_', ' ').capitalize()}"
        )
        scores = monte_carlo_simulation(num_games, strategy_class(), verbose)
        avg_score = np.mean(scores)
        results[strategy_name] = scores
        print(f"Average score after {num_games} games: {avg_score:.2f}")
    return results


def compare_strategies(results, strategies):
    print("\nStrategy Comparison:")
    best_strategy = min(strategies, key=lambda s: np.mean(results[s]))

    for strategy in strategies:
        if strategy != best_strategy:
            t_stat, p_value = stats.ttest_ind(results[best_strategy], results[strategy])
            diff = np.mean(results[strategy]) - np.mean(results[best_strategy])
            print(
                f"{best_strategy.replace('_', ' ').capitalize()} vs {strategy.replace('_', ' ')}:"
            )
            print(f"  Difference: {diff:.2f} points")
            print(f"  p-value: {p_value:.4f}")
            print(
                f"  {'Statistically significant' if p_value < 0.05 else 'Not statistically significant'}"
            )

    print(f"\nThe best strategy is: {best_strategy.replace('_', ' ').capitalize()}")


# Run simulations
num_games = 500_000

# uncomment to print the hands of a single run of each strategy
# num_games = 1

print_hands = num_games == 1
strategies = {
    "same_column": SameColumnStrategy,
    "different_columns": DifferentColumnsStrategy,
    "flip_if_first_not_two": HybridStrategy,
}
results = run_simulations(num_games, strategies, print_hands)

if not print_hands:
    compare_strategies(results, strategies.keys())
