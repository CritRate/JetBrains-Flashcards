# Write your code here
import argparse
import random

cards = {}
log = []


def print_message(message):
    log.append(message)
    print(message)


def user_input(question):
    log.append(question)
    return input(question)


def menu():
    while True:
        user_inp = user_input('Input the action (add, remove, import, export, ask, exit, '
                              'log, hardest card, reset stats):\n')
        if user_inp in ['add', 'remove', 'import', 'export', 'ask',
                        'exit', 'log', 'hardest card', 'reset stats']:
            return user_inp


def add_card():
    while True:
        term = user_input('The card:\n')

        if term in cards:
            print_message(f'The card "{term}" already exists.\n')
            continue
        break

    while True:
        definition = user_input('The definition of the card:\n')

        if definition in [definition['definition'] for key, definition in cards.items()]:
            print_message(f'The definition "{definition}" already exists.\n')
            continue
        break

    cards[term] = {
        'definition': definition,
        'wrong': 0
    }
    print_message(f'The pair ("{term}":"{definition}") has been added.\n')


def remove_card():
    card_to_remove = user_input('Which card?\n')

    if card_to_remove in cards:
        cards.pop(card_to_remove)
        print_message('The card has been removed.')
    else:
        print_message(f'Can\'t remove "{card_to_remove}": there is no such card.')


def import_cards(filename=None):
    if not filename:
        filename = user_input('File name:\n')

    try:
        with open(filename, 'r') as file:
            added_cards = 0
            for card in file.read().split('\n'):
                if card:
                    added_cards += 1
                    term, definition, wrong = card.split(':')
                    cards[term] = {
                        'definition': definition,
                        'wrong': int(wrong)
                    }
        print_message(f'{added_cards} cards have been loaded.')
    except FileNotFoundError:
        print_message('File not found.')


def export_cards(filename=None):
    if not filename:
        filename = user_input('File name:\n')

    with open(filename, 'w') as file:
        added_cards = 0
        for term, definition in cards.items():
            added_cards += 1
            file.write(f'{term}:{definition["definition"]}:{definition["wrong"]}\n')
    print_message(f'{added_cards} cards have been saved.')


def ask():
    number_of_questions = int(user_input('How many times to ask?\n'))

    questions = list()

    for _ in range(number_of_questions):
        questions.append(random.choice(list(cards)))

    for question in questions:
        answer = user_input(f'Print the definition of "{question}":\n')

        if answer in [definition['definition'] for key, definition in cards.items()]:
            if answer == cards[question]['definition']:
                print_message('Correct!')
            else:
                print_message(
                    f'Wrong. The right answer is "{cards[question]["definition"]}", but your definition is correct '
                    f'for "{[key for key, value in cards.items() if value["definition"] == answer][0]}".')
                cards[question]['wrong'] += 1
        else:
            print_message(f'Wrong. The right answer is "{cards[question]["definition"]}"')
            cards[question]['wrong'] += 1


def logs():
    filename = user_input('File name:\n')

    with open(filename, 'w') as file:
        for line in log:
            file.write(f'{line}\n')
    print_message(f'The log has been saved.')


def hardest_card():
    highest_wrong_score = 0
    wrong_questions = list()
    for term, card in cards.items():
        if card['wrong'] == highest_wrong_score:
            wrong_questions.append(f'"{term}"')
        if card['wrong'] > highest_wrong_score:
            highest_wrong_score = card['wrong']
            wrong_questions.clear()
            wrong_questions.append(f'"{term}"')
    if highest_wrong_score == 0:
        print_message('There are no cards with errors.')
    else:
        print_message(
            f'The hardest card is {", ".join(wrong_questions)}.'
            f'You have {highest_wrong_score} errors answering it.')


def reset_stats():
    for _, card in cards.items():
        card['wrong'] = 0
    print_message('Card statistics has been reset.')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--import_from', help='import cards from file', type=str)
    parser.add_argument('--export_to', help='export cards to specified text file after exiting', type=str)
    args = parser.parse_args()

    if args.import_from:
        import_cards(filename=args.import_from)

    while True:
        option = menu()

        if option == 'add':
            add_card()
        if option == 'remove':
            remove_card()
        if option == 'import':
            import_cards()
        if option == 'export':
            export_cards()
        if option == 'ask':
            ask()
        if option == 'log':
            logs()
        if option == 'hardest card':
            hardest_card()
        if option == 'reset stats':
            reset_stats()
        if option == 'exit':
            if args.export_to:
                export_cards(filename=args.export_to)
            print_message('Bye bye!')
            break
