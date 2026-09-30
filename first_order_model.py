# The max_steps=20 is not changing the language model itself. It is just a safety mechanism for generation.

# With your dataset, greedy generation can enter this cycle:

# the -> cat -> sat -> on -> the -> cat -> sat -> on -> ...

# because the model makes every decision using only the previous word.

# greedy decoding can get stuck in repetitive cycles in a first-order Markov language model.

# Sampling, on the other hand, can generate different paths because it randomly chooses according to the learned probabilities.

import random
from collections import defaultdict

# Training data
sentences = [
    ["<START>", "the", "cat", "sat", "on", "the", "mat", "<END>"],
    ["<START>", "the", "cat", "sat", "on", "the", "rug", "<END>"],
    ["<START>", "the", "dog", "sat", "on", "the", "mat", "<END>"],
    ["<START>", "the", "dog", "ran", "to", "the", "park", "<END>"],
    ["<START>", "the", "cat", "ran", "to", "the", "park", "<END>"],
    ["<START>", "the", "dog", "sat", "on", "the", "rug", "<END>"]
]

# 1. Count transitions between consecutive tokens
transition_counts = defaultdict(lambda: defaultdict(int))

for sentence in sentences:
    for i in range(len(sentence) - 1):
        current_token = sentence[i]
        next_token = sentence[i + 1]
        transition_counts[current_token][next_token] += 1


# 2. Construct conditional probability distribution P(next | current)
probabilities = {}

for current_token, next_tokens in transition_counts.items():
    total = sum(next_tokens.values())
    probabilities[current_token] = {}

    for next_token, count in next_tokens.items():
        probabilities[current_token][next_token] = count / total


# 3. Display probabilities for a specified previous token
def display_probabilities(previous_token):
    if previous_token not in probabilities:
        print("No transitions found for:", previous_token)
        return

    print("Probabilities after:", previous_token)

    for next_token, probability in probabilities[previous_token].items():
        print(f"P({next_token} | {previous_token}) = {probability:.3f}")


# 4. Predict the most probable next token
def predict_next(previous_token):
    if previous_token not in probabilities:
        return None

    return max(
        probabilities[previous_token],
        key=probabilities[previous_token].get
    )


# 5. Generate a sentence using greedy or sampling mode
def generate_sentence(mode, max_steps=20):
    current_token = "<START>"
    generated_tokens = []

    # Maximum number of steps prevents infinite loops
    for _ in range(max_steps):

        # Stop if END token is generated
        if current_token == "<END>":
            break

        # Get possible next tokens and their probabilities
        next_tokens = list(probabilities[current_token].keys())
        next_probabilities = list(probabilities[current_token].values())

        if mode == "greedy":
            # Mode A: Always choose the most probable next token
            next_token = max(
                probabilities[current_token],
                key=probabilities[current_token].get
            )

        elif mode == "sampling":
            # Mode B: Sample according to the probability distribution
            next_token = random.choices(
                next_tokens,
                weights=next_probabilities,
                k=1
            )[0]

        else:
            raise ValueError("Mode must be 'greedy' or 'sampling'")

        # Do not include <END> in the displayed sentence
        if next_token != "<END>":
            generated_tokens.append(next_token)

        current_token = next_token

    return " ".join(generated_tokens)


# Display probabilities
display_probabilities("the")


# Predict the most probable next token
print("\nMost probable next token after 'cat':",
      predict_next("cat"))


# Generate five sentences using Greedy mode
print("\nMode A: Greedy Generation")

for i in range(5):
    print(generate_sentence("greedy"))


# Generate five sentences using Sampling mode
print("\nMode B: Sampling Generation")

for i in range(5):
    print(generate_sentence("sampling"))


# 6. Check that probability distributions sum to 1
print("\nChecking probability normalization:")

for word in probabilities:
    total = sum(probabilities[word].values())
    print(word, total)

    # Allow a small floating-point error
    assert abs(total - 1.0) < 1e-9

print("All probability distributions are correctly normalized.")