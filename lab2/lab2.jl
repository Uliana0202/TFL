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
            print(rpad("\"" * table[i][j] * "\"", 10))
        end
        println()
    end
    println()
end

function generate_strings(len, current_string="")
    if len == 0
        return [current_string]
    end
    strings = []
    for c in ['L', 'R']
        append!(strings, generate_strings(len - 1, current_string * c))
    end
    return strings
end

function make_extension!(table, pref, n)
    for i in 1:n
        strings = generate_strings(i)
        for s in strings
            push!(table, fill("0", size(table[1])))
            table[end][1] = pref * s
        end
    end
end

function solve_incompleteness!(table, pos_unchecked, start_extension, coef_extension)
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
        
        len_0 = length(table)
        for i in 0:(start_extension - start_extension_0 - 1)
            make_extension!(table, table[start_extension_0 + i][1], coef_extension)
        end
        
        full_rows!(table, len_0 + 1)
        flag, start_extension = solve_incompleteness!(table, length(table) - 2 * (start_extension - start_extension_0) + 1, start_extension, coef_extension)
        if flag
            return true, start_extension
        end
    end
end

function main()
    table = [
        ["", ""],
        ["", "0"]
    ]
    coef_extension = 1
    start_extension = 3
    make_extension!(table, table[1][2], coef_extension)
    full_rows!(table, 2)
    
    while true
        _, start_extension = solve_incompleteness!(table, start_extension, start_extension, coef_extension)
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
