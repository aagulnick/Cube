# INSTRUCTIONS:
# Ensure the file paths below are accurate.
# Go to a cube in CubeKoga: Overview > Export > Copy to Clipboard.
# Paste into cube_list.txt.

import random
MEMORY = r"C:\python\Cube\draft_results.txt"
CUBE_LIST_FILE = r"C:\python\Cube\cube_list.txt"
CARDS_PER_PACK = 8

with open(CUBE_LIST_FILE, "r") as f:
    cube_list = f.read()

# process cube card list

lst = cube_list.split("\n")

lst[:] = [x for x in lst if x]  # remove all empty strings, in case I left a blank line or placed the quotes wrong

final_list = []
for s in lst:
    num, card = s.split(" ", 1)
    for _ in range(int(num)):
        final_list.append(card)

# Actual drafting code below

def draw_pack(stack, n):
    """Given a stack of cards, draw a pack of n cards to be drafted from."""
    pack = []
    to_choose_from = list(stack)  # make a copy so we don't mutate the argument unexpectedly
    for i in range(min(n, len(to_choose_from))):
        card = random.choice(to_choose_from)
        to_choose_from.remove(card)
        pack.append(card)
    return pack


def solomon_draft(cube, n):
    player_1_cards = []
    player_2_cards = []
    unchosen = list(cube)
    while len(unchosen) > 0:
        pack = draw_pack(unchosen, n)
        for card in pack:
            unchosen.remove(card)

        n = len(pack)
        for i in range(n):
            print(f"{i}: {pack[i]}")

        confirmed = "N"
        while not confirmed == "Y":
            pile_1 = input("Which cards go into pile 1? ").split(" ")  # indices should be input as a sequence of numbers separated by whitespace
            try:
                indices = [int(k) for k in pile_1]
                pile_1_cards = [pack[k] for k in indices]
                pile_2_cards = [pack[k] for k in range(n) if k not in indices]
                confirmed = input("Pile 1 will be: \n{0}\nPile 2 will be: \n{1}\nPlease confirm with 'Y' if this is correct. ".format('\n'.join(pile_1_cards), '\n'.join(pile_2_cards)))
            except:
                print(f"Error processing pile split. Please type in a sequence of indices between {0} and {n-1} separated by whitespace.")

        confirmed_2 = "N"
        while not confirmed_2 == "Y":
            try:
                player_1_pile = int(input("Which pile should be given to player 1? "))
                if player_1_pile == 1:
                    player_1_cards = player_1_cards + pile_1_cards
                    player_2_cards = player_2_cards + pile_2_cards
                elif player_1_pile == 2:
                    player_1_cards = player_1_cards + pile_2_cards
                    player_2_cards = player_2_cards + pile_1_cards
                else:
                    raise ValueError("Input was not either 1 or 2 (but was an integer).")

                confirmed_2 = input(f"Giving player 1 pile {player_1_pile}. Is this correct? Please confirm by typing 'Y'. ")
            except:
                print("Error processing pile choice. Please only type either 1 or 2.")

        if len(unchosen) > 0:
            print(f"Player 1 now has {len(player_1_cards)} cards: {player_1_cards} \nPlayer 2 has {len(player_2_cards)}: {player_2_cards}.")
            input(f"Press enter when ready for next pack. There are {len(unchosen)} cards left.")

    print(f"Player 1 drafted: {player_1_cards} \nPlayer 2 drafted: {player_2_cards}")
    return player_1_cards, player_2_cards

drafts = solomon_draft(final_list, CARDS_PER_PACK)

def remove_non_ascii(text):
    """Strips non-ASCII characters, like delta and prism star, from card names so that file.write doesn't error."""
    return ''.join([i for i in text if ord(i) < 128])

with open(MEMORY, 'w') as file:
    p1_cards = drafts[0]
    p2_cards = drafts[1]
    p1_cards_untap_formatted = [str(p1_cards.count(card))+ " " + str(card) for card in set(p1_cards)]
    p2_cards_untap_formatted = [str(p2_cards.count(card))+ " " + str(card) for card in set(p2_cards)]
    file.write(remove_non_ascii("PLAYER 1: \n{0}\n\nPLAYER 2: \n{1}".format('\n'.join(p1_cards_untap_formatted), '\n'.join(p2_cards_untap_formatted))))
