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

function full_rows!(start_pref, table)
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

function generate_strings(len, current_string)
    if len == 0
        return [current_string]
    end
    strings = []
    for c in ['L', 'R']
        append!(strings, generate_strings(len - 1, current_string * c))
    end
    return strings
end

function does_not_meet_pref(table, pref, start)
    for i in start:length(table)
        if table[i][1] == pref
            return false
        end
    end
    return true
end

function make_checked_extension!(table, pref, n, start)
    strings = generate_strings(n, "")
    extended = 0
    for s in strings
        if does_not_meet_pref(table, pref * s, start)
            push!(table, ["0" for _ in 1:length(table[1])])
            table[end][1] = pref * s
            extended += 1
        end
    end
    full_rows!(length(table) - extended + 1, table)
    return extended
end

function make_extension!(table, pref, n)
    strings = generate_strings(n, "")
    for s in strings
        push!(table, fill("0", size(table[1])))
        table[end][1] = pref * s
    end
    full_rows!(length(table) - length(strings) + 1, table) 
    return length(strings)
end

function does_not_meet_row(table, finish, row)
  for i in 2:finish
    if table[i][2:end] == row
      return false
    end
  end
  return true
end

function solve_incompleteness!(table, pos_unchecked, start_extension, coef_ext)
    start_extension_0 = start_extension
    while true
        for i in pos_unchecked:length(table)
            if does_not_meet_row(table, start_extension - 1, table[i][2:end])
                table[i], table[start_extension] = table[start_extension], table[i]
                start_extension += 1
            end
        end
        
        if start_extension == start_extension_0
            return true, start_extension
        end
    
        extended = 0
        for i in start_extension_0:(start_extension - 1)
            extended += make_extension!(table, table[i][1], 1)
            if coef_ext > 1
                for j in 2:(coef_ext + 1)
                    extended += make_checked_extension!(table, table[i][1], coef_ext, i)
                end
            end
        end

    
        flag, start_extension = solve_incompleteness!(table, length(table) - extended, start_extension, coef_ext)
        if flag
            return true, start_extension
        end
    end
end


open("parameters.txt", "r") do file
    global num_of_vertices = parse(Int, split(strip(readline(file)))[1])
end
println(num_of_vertices)
table = [
    ["", ""],
    ["", "0"],
    ["L", "0"],
    ["R", "0"]
]
    
full_rows!(2, table)
start_extension = 3

requirement_for_extra = 5 * (start_extension - 2) < num_of_vertices
start_extra = 2
    
    
while true
    global start_extension, start_extra
    _, start_extension = solve_incompleteness!(table, start_extension, start_extension, 1)
    counter = 2
    
    while requirement_for_extra && counter < 4
        for i in start_extra:(start_extension - 1)
            make_checked_extension!(table, table[i][1], counter, i)
        end
        
        _, start_extension = solve_incompleteness!(table, start_extra, start_extension, counter)
        counter += 1
    end
    
    start_extra = start_extension
    guessed, counterexample = is_equivalent(table, start_extension)
        
    if guessed
        break
    end
        
    for i in 1:length(counterexample)
        push!(table[1], counterexample[1:i])
    end
        
    for i in 2:length(table)
        append!(table[i], ["0" for _ in 1:length(counterexample)])
        for j in (length(table[1]) - length(counterexample) + 1):length(table[1])
            table[i][j] = is_member(table[i][1] * table[1][j])
            if table[i][j] == "1"
                break
            end
        end
    end
end

print_table(table, start_extension)
