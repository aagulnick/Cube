# INSTRUCTIONS:
# Ensure the file paths below are accurate.
# Go to a cube in CubeKoga: Overview > Export > Copy to Clipboard.
# Paste into cube_list.txt.
# Have both players load this program and play in parallel, sharing seeds via Discord or another communication method.
# an implementation of Winston drafting where piles are face-down, so seeds must be used to communicate between players.

import random
MEMORY = r"C:\python\functions\drafts.txt"
CUBE_LIST_FILE = r"C:\python\Cube\cube_list.txt"

with open(CUBE_LIST_FILE, "r") as f:
    cube_list = f.read()

def p_valuation(n, p):
    """Given an integer n and a prime p, return the highest power of p dividing n."""
    count = 0
    while n % p == 0:
        n = n % p
        count += 1
    return count


def remove_non_ascii(text):
    """Strips non-ASCII characters, like delta and prism star, from card names so that file.write doesn't error."""
    return ''.join([i for i in text if ord(i) < 128])


def draw_piles(cube):
    """NOTE: Mutates the list CUBE"""
    piles = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            card = random.choice()
            piles[i].append

    pile_2 = [random.choice(cube) for _ in range(4)]
    for card in pile_2:
        cube.remove(card)
    pile_3 = [random.choice(cube) for _ in range(4)]
    pile_4 = [random.choice(cube) for _ in range(4)]

    for card in pile_3:
        cube.remove(card)
    for card in pile_4:
        cube.remove(card)

    return [pile_1, pile_2, pile_3, pile_4]

def seeded_draw_piles(cube, seed):
    """Given a collection of 16 seeds, draw 4 piles using the seed. Mutates the CUBE list."""
    assert len(seed) == 16, "Must supply 16 seeds."
    cards = [[], [], [], []]
    for i in range(16):
        random.seed(seed[i])
        if len(cube) > 0:
            card = random.choice(cube)
            cards[i % 4].append(card)
            cube.remove(card)
    return cards

def ask_for_confirmed_input(message, processing_function):
    confirmed = False
    while not confirmed:
        try:
            inp = input(message)
            result = processing_function(inp)
            confirmed = (input("Please confirm with Y: ") == "Y")
        except:
            print("Error. Please try again.")

    return result

# process cube card list

lst = cube_list.split("\n")

def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

final_list = []
for s in lst:
    index = find_nth(s, "\t", 3)
    final_list.append(s[:index].replace("\t", " "))

# Actual code below

cube = list(final_list)
my_cards = []
opp_cards = []

unchosen = list(cube)

first_player = input("Are you going first? ")
if first_player == "Y":
    my_turn = True
    print("You will pick first.")
else:
    my_turn = False
    print("Your opponent will pick first.")

piles = []

while len(unchosen) > 0 or len(piles) > 0:
    # set up the piles if there are none existing
    if len(piles) == 0:
        if my_turn:
            seed = [random.randint(0, 2**8 - 1) for _ in range(16)]
            ask_for_confirmed_input(f"Please give your opponent the following seed: {seed}", lambda x: x)
        else:
            seed = ask_for_confirmed_input("Please input the seed from your opponent: ", lambda x: [int(n) for n in x.split(', ')])
        piles = seeded_draw_piles(unchosen, seed)
    # one player chooses a pile
    if my_turn:
        for i in range(len(piles)):
            print(f"Pile {i + 1}: {', '.join(piles[i])}")
        chosen_pile = ask_for_confirmed_input("Which pile will you take? ", lambda x: piles[int(x) - 1])
        my_cards = my_cards + chosen_pile
        seed = [random.randint(0, 2**8 - 1), random.randint(0, 2**8 - 1), random.randint(0, 2**8 - 1)]
        ask_for_confirmed_input(f"Please give your opponent the following seed, and press enter when ready:\n{seed[0], seed[1], seed[2]}", lambda x: x)
    else:
        chosen_pile = ask_for_confirmed_input("Which pile is your opponent taking? ", lambda x: piles[int(x) - 1])
        opp_cards = opp_cards + chosen_pile
        seed = ask_for_confirmed_input("Please input the seed your opponent gives you for the next draw: ", lambda x: [int(n) for n in x.split(', ')])

    piles.remove(chosen_pile)
    for pile, sd in zip(piles, seed[:len(piles)]):
        random.seed(sd)
        if len(unchosen) > 0:  # otherwise don't add to the piles
            card = random.choice(unchosen)
            pile.append(card)
            unchosen.remove(card)

    if my_turn:
        print(f"You now have: {my_cards}")
        with open(MEMORY, 'w') as file:
            file.write(remove_non_ascii("My cards: \n{0}".format('\n'.join(my_cards))))
    if len(piles) > 0:
        my_turn = not my_turn
    print(f"There are {len(unchosen)} cards left in the deck. There are {len(piles)} piles left.")

# when all cards are drafted
with open(MEMORY, 'w') as file:
    file.write(remove_non_ascii("My cards: \n{0}\n\nOpponent's cards: \n{1}".format('\n'.join(my_cards), '\n'.join(opp_cards))))
