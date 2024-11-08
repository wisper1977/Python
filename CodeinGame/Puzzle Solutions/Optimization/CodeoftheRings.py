alphabet = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"

PLUS = "+"
MINUS = "-"
FORWARD = ">"
BACKWARD = "<"
TRIGGER = "."
position = 0


def main():
    global position
    magic_phrase = input().strip()

    fields = [" "] * 30
    shortest = ""

    for c in magic_phrase:
        best = find_shortest(alphabet.index(c), fields)
        shortest += best

        steps_needed = steps(best)

        # Update position based on the number of steps
        if steps_needed < 0 and position + steps_needed < 0:
            position = 30 - (abs(steps_needed) + position)
        elif steps_needed > 0 and position + steps_needed > 29:
            steps_needed = 30 - position
            position = steps_needed
        else:
            position += steps_needed

        fields[position] = c

    print(shortest)


def find_shortest(magic_index, fields):
    global position
    tmp = position
    best = ""
    
    # Loop to find the shortest path clockwise
    while True:
        result = ""
        
        if tmp == position:
            result = trigger(letter_distance(fields[tmp], magic_index))
        elif position < tmp:
            result += FORWARD * (tmp - position)
            result += trigger(letter_distance(fields[tmp], magic_index))
        else:
            result += FORWARD * (30 - position + tmp)
            result += trigger(letter_distance(fields[tmp], magic_index))

        tmp += 1
        if tmp == 30:
            tmp = 0
        if tmp == position:
            break

        if not best or len(result) <= len(best):
            best = result

    # Loop to find the shortest path counter-clockwise
    tmp = position
    while True:
        result = ""
        
        if tmp == position:
            result = trigger(letter_distance(fields[tmp], magic_index))
        elif tmp < position:
            result += BACKWARD * (position - tmp)
            result += trigger(letter_distance(fields[tmp], magic_index))
        else:
            result += BACKWARD * (30 - position + tmp)
            result += trigger(letter_distance(fields[tmp], magic_index))

        tmp -= 1
        if tmp == -1:
            tmp = 29
        if tmp == position:
            break

        if not best or len(result) <= len(best):
            best = result

    return best


def trigger(limit):
    result = ""
    for _ in range(abs(limit)):
        result += MINUS if limit <= 0 else PLUS
    return result + TRIGGER


def letter_distance(start, dest):
    start_position = alphabet.index(start)
    
    if start_position < dest:
        spin_up = dest - start_position
        spin_down = 27 - dest + start_position
        return spin_up if spin_up <= spin_down else -spin_down
    elif start_position > dest:
        spin_up = 27 - start_position + dest
        spin_down = start_position - dest
        return spin_up if spin_up <= spin_down else -spin_down
    
    return 0


def steps(instructions):
    return instructions.count(FORWARD) - instructions.count(BACKWARD)


if __name__ == "__main__":
    main()
