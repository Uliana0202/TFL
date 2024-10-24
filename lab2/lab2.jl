function is_equivalent(table, start_extension)
    println("Is it right?")
    print_table(table, start_extension)
    flag = parse(Bool, readline())
    counterexample = readline()
    return flag, counterexample
end

function is_member(str)
  print("Does \"", str, "\" help to escape?: ")
  res = readline()
  return  res
end



function full_rows!(table, start_pref)
    for i in start_pref:length(table)
        for j in 2:length(table[1])
            table[i][j] = is_member(table[i][1] * table[1][j])
        end
    end
end

function print_table(table, start_extension)
    for i in 1:length(table)
        if i == start_extension
            println("____________")
        end
        for j in 1:length(table[1])
            print(rpad("\"" * table[i][j] * "\"", 5))
        end
        println()
    end
    println()
end

function solve_incompleteness!(table, pos_unchecked, start_extension)
    start_extension_0 = start_extension
    while true
        for i in pos_unchecked:length(table)
            do_not_meet = true
            j = 1
            while j < start_extension && do_not_meet
                if table[i][2:end] == table[j][2:end]
                    do_not_meet = false
                end
                j += 1
            end
            if do_not_meet
                table[i], table[start_extension] = table[start_extension], table[i]
                start_extension += 1
            end
        end
        if start_extension == start_extension_0
            return true, start_extension
        end
        for i in 1:(start_extension - start_extension_0)
            push!(table, ["0" for _ in 1:length(table[1])])
            table[end][1] = table[start_extension_0 + i - 1][1] * "L"
            push!(table, ["0" for _ in 1:length(table[1])])
            table[end][1] = table[start_extension_0 + i - 1][1] * "R"
        end
        full_rows!(table, length(table) - 2 * (start_extension - start_extension_0) + 1)
        flag, start_extension = solve_incompleteness!(table, length(table) - 2 * (start_extension - start_extension_0) + 1, start_extension)
        if flag
            return true, start_extension
        end
    end
end

function main()
    table = [
        ["", ""],
        ["", "0"],
        ["L", "0"],
        ["R", "0"]
    ]
    start_extension = 3
    full_rows!(table, 2)
    
    while true
        _, start_extension = solve_incompleteness!(table, start_extension, start_extension)
        guessed, counterexample = is_equivalent(table, start_extension)
        if guessed
            break
        end
        for i in 1:length(counterexample)
            push!(table[1], counterexample[1:i])
            for j in 2:length(table)
                push!(table[j], is_member(table[j][1] * counterexample[1:i]))
            end
        end
    end
    print_table(table, start_extension)
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end