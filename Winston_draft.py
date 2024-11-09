# INSTRUCTIONS:
# Ensure the file paths below are accurate.
# Go to a cube in CubeKoga: Overview > Export > Copy to Clipboard.
# Paste into cube_list.txt.
# Have both players load this program and play in parallel, sharing seeds via Discord or another communication method.
# an implementation of Winston drafting where piles are face-down, so seeds must be used to communicate between players.
# Key difference: cannot opt to take top card of the deck instead. You must take the last pile if it comes to that.

import random
MEMORY = r"C:\python\functions\drafts.txt"
CUBE_LIST_FILE = r"C:\python\Cube\cube_list.txt"
STARTING_PILE_SIZE = 4
NUM_PILES = 4

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


def seeded_draw_piles(cube, seed):
    """Given a collection of 16 seeds, draw 4 piles using the seed. Mutates the CUBE list."""
    assert len(seed) == NUM_PILES*STARTING_PILE_SIZE, "Must supply 16 seeds."
    cards = [[] for _ in range(NUM_PILES)]
    for i in range(NUM_PILES*STARTING_PILE_SIZE):
        if len(cube) > 0:
            random.seed(seed[i])
            card = random.choice(cube)
            cards[i % NUM_PILES].append(card)
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
            seed = [random.randint(0, 2**8 - 1) for _ in range(NUM_PILES*STARTING_PILE_SIZE)]
            ask_for_confirmed_input(f"Please give your opponent the following seed:\n{', '.join([str(s) for s in seed])}", lambda x: x)
        else:
            seed = ask_for_confirmed_input("Please input the seed from your opponent: ", lambda x: [int(n) for n in x.split(', ')])
        piles = seeded_draw_piles(unchosen, seed)
    # one player chooses a pile
    if my_turn:
        taking = ""
        pile_num = -1
        while not (taking == "Y"):
            pile_num += 1
            if pile_num < len(piles) - 1:
                print(f"Pile {pile_num + 1} contains: {', '.join(piles[pile_num])}")
                taking = ask_for_confirmed_input("Will you take this pile? Y or N: ", lambda x: x)
            else:
                print(f"You take the last pile: {', '.join(piles[pile_num])}")
                taking = "Y"
        chosen_pile = piles[pile_num]
        my_cards = my_cards + chosen_pile
        seed = [random.randint(0, 2**8 - 1) for _ in range(len(piles) - 1)]  # we will be removing one pile before the opponent uses this seed
        ask_for_confirmed_input(f"Please give your opponent the following seed, and press enter when ready:\n{', '.join([str(seed[n]) for n in range(len(piles) - 1)])}", lambda x: x)
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
