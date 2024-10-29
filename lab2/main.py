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
    extended = 0
    for i in range(n):
        strings = generate_strings(i + 1, "")
        for s in strings:
            table.append(["0" for _ in range(len(table[0]))])
            table[-1][0] = pref + s
            extended += 1
        full_rows(len(table) - len(strings), table)
    return extended
    
def does_not_meet(table, finish, row):
    for i in range(1, finish):
        if table[i][1:] == row:
            return False
    return True


def solve_incompleteness(table, pos_unchecked, start_extension, coef_ext):
    start_extension_0 = start_extension
    while True:
        for i in range(pos_unchecked, len(table)):
            if does_not_meet(table, start_extension, table[i][1:]):
                table[i], table[start_extension] = table[start_extension], table[i]
                start_extension += 1

        if start_extension == start_extension_0:
            return True, start_extension

        extended = 0
        for i in range(start_extension - start_extension_0):
            extended += make_extension(table, table[start_extension_0 + i][0], coef_ext)

        flag, start_extension = solve_incompleteness(table, len(table) - extended, start_extension, coef_ext)
        if flag:
            return True, start_extension
def main():
    num_of_vertices = 160  ################### Read from a file
    table = [
        ["", ""],
        ["", "0"]
    ]
    table[1][1] = is_member("")
    make_extension(table, table[1][0], 1)
    start_extension = 2
    print_table(table, start_extension)


    requirement_for_extra = 5*(start_extension - 1) < num_of_vertices
    len_extra = len(table[-1][0])

    while True:
        _, start_extension = solve_incompleteness(table, start_extension, start_extension, 1)
        start_extra = start_extension
        print_table(table, start_extension)

        # SxSigma быстро возрастает, поэтому ставлю предел в 2 дополительных расширения
        counter = 1
        while counter < 3 and requirement_for_extra and len(table[0]) > 2:
            len_0 = len(table)
            extended = 0
            for j in range(start_extra, len_0):
                if len(table[j][0]) >= len_extra:
                    extended += make_extension(table, table[j][0], 1)
            counter += 1
            start_extra = len(table) - extended
            _, start_extension = solve_incompleteness(table, start_extra, start_extension, counter)
            len_extra += 1

        start_extra = len(table) # Дальше дополнительно расширять мне надо только те части таблицы, которые получились из нового класса и дописанных L, R
        len_extra = len(table[-1][0])
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
