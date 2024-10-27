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

def generate_strings(len, current_string):
    if len == 0:
        return [current_string]

    strings = []
    for c in ['L', 'R']:
        strings.extend(generate_strings(len - 1, current_string + c))

    return strings
def make_extension(table, pref, n):
    for i in range(n):
        strings = generate_strings(i+1, "")
        for s in strings:
            table.append(["0" for _ in range(len(table[0]))])
            table[-1][0] = pref + s


def solve_incompleteness(table, pos_unchecked, start_extension, coef_extension):
    start_extension_0 = start_extension
    while True:
        for i in range(pos_unchecked, len(table)):
            do_not_meet = True
            j = 1
            while j < start_extension and do_not_meet:
                if table[i][1:] == table[j][1:]:
                    do_not_meet = False
                j += 1

            if do_not_meet:
                table[i], table[start_extension] = table[start_extension], table[i]
                start_extension += 1

        if start_extension == start_extension_0:
            return True, start_extension

        len_0 = len(table)
        for i in range(start_extension - start_extension_0):
            make_extension(table, table[start_extension_0 + i][0], coef_extension)

        full_rows(len_0, table)

        flag, start_extension = solve_incompleteness(table, len(table) - 2 * (start_extension - start_extension_0), start_extension, coef_extension)
        if flag:
            return True, start_extension


def main():
    table = [
        ["", ""],
        ["", "0"]
    ]
    coef_extension = 1
    start_extension = 2
    make_extension(table, table[0][1], coef_extension)
    full_rows(1, table)

    while True:
        _, start_extension = solve_incompleteness(table, start_extension, start_extension, coef_extension)
        guessed, counterexample = is_equivalent(table, start_extension)

        if guessed:
            break

        for i in range(1, len(counterexample)+1):
            table[0].append(counterexample[:i])
            for j in range(1, len(table)):
                table[j].append(is_member(table[j][0] + counterexample[:i]))

    print_table(table, start_extension)

if __name__ == '__main__':
    main()
