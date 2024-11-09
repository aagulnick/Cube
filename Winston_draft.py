# INSTRUCTIONS:
# Ensure the file paths below are accurate.
# Go to a cube in CubeKoga: Overview > Export > Copy to Clipboard.
# Paste into cube_list.txt.
# Have both players load this program and play in parallel, sharing seeds via Discord or another communication method.
# an implementation of Winston drafting where piles are face-down, so seeds must be used to communicate between players.

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
    """Given a collection of NUM_PILES*STARTING_PILE_SIZE seeds, draw NUM_PILES piles of size STARTING_PILE_SIZE using the seed. Mutates the CUBE list."""
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

final_list[:] = [x for x in final_list if x]  # remove all empty strings, in case I left a blank line or placed the quotes wrong

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
    print(f"There are {len(unchosen)} cards left in the deck. There are {len(piles)} piles left.")
    # set up the piles if there are none existing
    if len(piles) == 0:
        if my_turn:
            seed = [random.randint(0, 2**8 - 1) for _ in range(NUM_PILES*STARTING_PILE_SIZE + 1)]
            ask_for_confirmed_input(f"Please give your opponent the following seed:\n{', '.join([str(s) for s in seed])}", lambda x: x)
        else:
            seed = ask_for_confirmed_input("Please input the seed from your opponent: ", lambda x: [int(n) for n in x.split(', ')])
        piles = seeded_draw_piles(unchosen, seed[:NUM_PILES*STARTING_PILE_SIZE])
        random.seed(seed[-1])
        next_card = [random.choice(unchosen)]
    # one player chooses a pile
    if my_turn:
        TOOK_TOP = False
        taking = ""
        pile_num = -1
        while not (taking == "Y"):
            pile_num += 1
            if pile_num < len(piles):
                print(f"Pile {pile_num + 1} contains: {', '.join(piles[pile_num])}")
                if pile_num == len(piles) - 1:
                    print("Warning: this is the last pile. If you do not take it, you will get the top card of the deck.")
                taking = ask_for_confirmed_input("Will you take this pile? Y or N: ", lambda x: x)
                chosen_pile = piles[pile_num]
            else:
                if not next_card:
                    print(f"The deck is empty, so you take the last pile: {', '.join(piles[pile_num - 1])}")
                    chosen_pile = piles[pile_num - 1]
                else:
                    print(f"You take the top card of the deck: {next_card[0]}")
                taking = "Y"
                chosen_pile = next_card
                TOOK_TOP = True
        my_cards = my_cards + chosen_pile
        seed = [random.randint(0, 2**8 - 1) for _ in range(len(piles) + int(TOOK_TOP))]  # we will be removing one pile before the opponent uses this seed, as long as we didn't take the top card
        ask_for_confirmed_input(f"Please give your opponent the following seed, and press enter when ready:\n{', '.join([str(s) for s in seed])}", lambda x: x)
    else:
        TOOK_TOP = False
        def choice_func(n, s):
            if n == 0:
                random.seed(s)
                return [random.choice(unchosen)], True
            else:
                return piles[n - 1], False
        chosen_pile, TOOK_TOP = ask_for_confirmed_input("Which pile is your opponent taking? (Use 0 for top card of deck) ", lambda x: choice_func(int(x), seed[-1]))
        opp_cards = opp_cards + chosen_pile
        seed = ask_for_confirmed_input("Please input the seed your opponent gives you for the next draw: ", lambda x: [int(n) for n in x.split(', ')])

    if not TOOK_TOP:
        piles.remove(chosen_pile)
    else:
        unchosen.remove(next_card[0])  # actually remove the top card from the deck iff it is taken

    assert len(seed) == len(piles) + 1, "Number of seeds does not match number of piles + 1 (for top of deck)! Clients must be desynced."  # we should always have enough seeds to add to the remaining piles, plus one for the top card of the deck
    for pile, sd in zip(piles, seed[:len(piles)]):
        # print(f"Using seed {sd}")
        random.seed(sd)
        if len(unchosen) > 0:  # otherwise don't add to the piles
            card = random.choice(unchosen)
            pile.append(card)
            unchosen.remove(card)
    next_card = []
    if len(unchosen) > 0:  # after the piles are lengthened
        # print(f"Using seed {seed[-1]}")
        random.seed(seed[-1])
        next_card = [random.choice(unchosen)]

    if my_turn:
        print(f"You now have: {my_cards}")
        with open(MEMORY, 'w') as file:
            file.write(remove_non_ascii("My cards: \n{0}".format('\n'.join(my_cards))))
    if len(piles) > 0:
        my_turn = not my_turn

# when all cards are drafted
with open(MEMORY, 'w') as file:
    file.write(remove_non_ascii("My cards: \n{0}\n\nOpponent's cards: \n{1}".format('\n'.join(my_cards), '\n'.join(opp_cards))))
