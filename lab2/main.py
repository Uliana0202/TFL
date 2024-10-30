def is_equivalent(table, start_extension):
    print("Is it right?")
    print_table(table, start_extension)
    flag = input()
    counterexample = input()
    return flag, counterexample
def is_member(str):
    return input(f"Does \"{str}\" help to escape? ")

def full_rows(start_pref, table):
    for i in range(start_pref, len(table)):
        for j in range(1, len(table[0])):
            table[i][j] = is_member(table[i][0] + table[0][j])

def print_table(table,start_extension):
    for i in range(len(table)):
        if i == start_extension:
            print("____________")
        for j in range(len(table[0])):
            print('{:>10}'.format("\"" + table[i][j] +"\""), end="")
        print()
    print()


def generate_strings(n, current_string):
    if n == 0:
        return [current_string]
    strings = []
    for c in ['L', 'R']:
        strings.extend(generate_strings(n - 1, current_string + c))
    return strings

def does_not_meet_pref(table, pref, start):
    for i in range(start, len(table)):
        if table[i][0] == pref:
            return False
    return True

def make_checked_extension(table, pref, n, start):
    strings = generate_strings(n, "")
    extended = 0
    for s in strings:
        if does_not_meet_pref(table, pref + s, start):
            table.append(["0" for _ in range(len(table[0]))])
            table[-1][0] = pref + s
            extended += 1
    full_rows(len(table) - extended, table)
    return extended

def make_extension(table, pref, n):
    strings = generate_strings(n, "")
    for s in strings:
        table.append(["0" for _ in range(len(table[0]))])
        table[-1][0] = pref + s
    full_rows(len(table) - len(strings), table)
    return len(strings)

def does_not_meet_row(table, finish, row):
    for i in range(1, finish):
        if table[i][1:] == row:
            return False
    return True

def solve_incompleteness(table, pos_unchecked, start_extension, coef_ext):
    start_extension_0 = start_extension
    while True:
        for i in range(pos_unchecked, len(table)):
            if does_not_meet_row(table, start_extension, table[i][1:]):
                table[i], table[start_extension] = table[start_extension], table[i]
                start_extension += 1

        if start_extension == start_extension_0:
            return True, start_extension

        extended = 0
        for i in range(start_extension_0, start_extension):
            extended += make_extension(table, table[i][0], 1)
            if coef_ext > 1:
                for j in range(2, coef_ext + 1):
                    extended += make_checked_extension(table, table[i][0], coef_ext, i)

        flag, start_extension = solve_incompleteness(table, len(table) - extended, start_extension, coef_ext)
        if flag:
            return True, start_extension
def main():
    with open("parameters.txt", 'r') as file:
        num_of_vertices = int(file.readline().strip().split()[0])

    table = [
        ["", ""],
        ["", "0"],
        ["L", "0"],
        ["R", "0"]
    ]
    full_rows(1, table)
    start_extension = 2

    requirement_for_extra = 5*(start_extension - 1) < num_of_vertices
    start_extra = 1

    while True:
        _, start_extension = solve_incompleteness(table, start_extension, start_extension, 1)

        counter = 2
        # SxSigma быстро возрастает, поэтому ставлю предел в 2 дополнительных  расширения
        while requirement_for_extra and counter < 4:
            for i in range(start_extra, start_extension):
                make_checked_extension(table, table[i][0], counter, i)
            _, start_extension = solve_incompleteness(table, start_extra, start_extension, counter)
            counter += 1

        start_extra = start_extension
        guessed, counterexample = is_equivalent(table, start_extension)

        if guessed:
            break

        for i in range(1, len(counterexample)+1):
            table[0].append(counterexample[-i:])

        for i in range(1, len(table)):
            table[i].extend(["0"] * len(counterexample))
            for j in range(len(table[0]) - len(counterexample), len(table[0])):
                table[i][j] = is_member(table[i][0] + table[0][j])

    print_table(table, start_extension)


if __name__ == '__main__':
    main()

