# INSTRUCTIONS:
# Ensure the file paths and other settings below are accurate.
# Go to a cube in CubeKoga: Overview > Export > Copy to Clipboard.
# Paste into cube_list.txt.
# Have both players load this program and play in parallel, sharing seeds via Discord or another communication method.
# an implementation of Winston drafting where piles are face-down, so seeds must be used to communicate between players.

import random
MEMORY = r"C:\python\functions\drafts.txt"
CUBE_LIST_FILE = r"C:\python\Cube\cube_list.txt"
STARTING_PILE_SIZE = 1
NUM_PILES = 3

with open(CUBE_LIST_FILE, "r") as f:
    cube_list = f.read()

def remove_non_ascii(text):
    """Strips non-ASCII characters, like delta and prism star, from card names so that file.write doesn't error."""
    return ''.join([i for i in text if ord(i) < 128])


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

if my_turn:
    seed = random.randint(0, 2**32 - 1)
    ask_for_confirmed_input(f"Please give your opponent the following seed, and press enter when done:\n{seed}", lambda x: x)
else:
    seed = ask_for_confirmed_input(f"Please input the seed your opponent gave you: ", lambda x: int(x))

random.seed(seed)
random.shuffle(unchosen)

while len(unchosen) > 0 or len(piles) > 0:
    # set up the piles if there are none existing
    if len(piles) == 0:
        piles = [[] for _ in range(NUM_PILES)]
        for pile in piles:
            for _ in range(STARTING_PILE_SIZE):
                pile.append(unchosen.pop())

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
                if len(unchosen) == 0:
                    print(f"The deck is empty, so you take the last pile: {', '.join(piles[pile_num - 1])}")
                    chosen_pile = piles[pile_num - 1]
                else:
                    chosen_pile = [unchosen.pop()]
                    print(f"You take the top card of the deck: {chosen_pile[0]}")
                    TOOK_TOP = True
                taking = "Y"
        my_cards = my_cards + chosen_pile
    else:
        TOOK_TOP = False
        def choice_func(n):
            if n == 0:
                return [unchosen.pop()], True
            else:
                return piles[n - 1], False
        chosen_pile, TOOK_TOP = ask_for_confirmed_input("Which pile is your opponent taking? (Use 0 for top card of deck) ", lambda x: choice_func(int(x)))
        opp_cards = opp_cards + chosen_pile

    if not TOOK_TOP:
        piles.remove(chosen_pile)

    for pile in piles:
        if len(unchosen) > 0:  # otherwise don't add to the piles
            pile.append(unchosen.pop())

    if my_turn:
        print(f"You now have: {my_cards}")
        with open(MEMORY, 'w') as file:
            file.write(remove_non_ascii("My cards: \n{0}".format('\n'.join(my_cards))))
    my_turn = not my_turn

    print(f"There are {len(unchosen)} cards left in the deck. There are {len(piles)} piles left.")

# when all cards are drafted
with open(MEMORY, 'w') as file:
    file.write(remove_non_ascii("My cards: \n{0}\n\nOpponent's cards: \n{1}".format('\n'.join(my_cards), '\n'.join(opp_cards))))
