# Задание
## Условие
Угадыватель заранее знает оценку сверху на число ветвлений в
лабиринте и число выходов из него (читая из файла parameters.txt
два соответствующих числа). По этому же файлу MAT
генерирует граф, используя данные числа как оценку сверху.
Входной автомат — произвольный планарный граф с бинарным
ветвлением. Все тупиковые ветки — выходы из лабиринта. Путь в
лабиринте представляет собой последовательность инструкций в
алфавите {L, R}: указывающих на каждой развилке, идти направо
или налево.
Путь принадлежит языку, если строго выводит к выходу (т.е.
следуя инструкциям и начиная из стартового состояния, вы
попадаете в финальное состояние). Если путь остаётся в
лабиринте или содержит дополнительные инструкции после
попадания в финальное состояние, считается, что он языку не
принадлежит.
## Оптимизпация
Опережающий L*: если запросы эквивалентности очень дорогие, и есть высокий шанс, что эквивалентность еще не достигнута, то можно расширять таблицу не на один шаг, а больше

# Реализация
## Взаимодейсвие с МАТ
На данном этапе работу МАТ имитируют функции

```
function is_equivalent(table, start_extension)
    println("Is it right?")
    print_table(table, start_extension)
    flag = parse(Bool, readline())
    counterexample = readline()
    return flag, counterexample
end
```

```
function is_member(str)
  print("Does \"", str, "\" help to escape?: ")
  res = readline()
  return  res
end
```
## Проверка условия полноты
Проверка условия полноты реализована рекурсивно.
**start_extension** - индекс строчки, с которой начинается расширенная часть таблицы, 
**pos_unchecked** - индекс строчки в расширенной части, с которой начинаются еще не проверенные в контексте условия полноты строчки, 
**coef_ext** - число символов для дополнительного расширения (помимо основного в один символ).

```
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
```
Стоит отметить, что при дополнительном расширении, строчки в расширенной части могут дублироваться. Для решения этой проблемы реализована функция **make_checked_extension!(table, pref, n, start)**, которая исключает дублирование.

## Проверка условия непротиворечивости
Так как реализован алгоритм, при котором контрпример и все его суффиксы заносятся в E, то такая проверка не требуется, так как строки в SxE не могут быть одинаковыми.

## Основная часть программы
Предположением о том, что "есть высокий шанс, что эквивалентность еще не достигнута", является

```
requirement_for_extra = 5 * (start_extension - 2) < num_of_vertices
```

**start_extra** - индекс элнемента, который еще не проходил дополнительное расширение

Стоит отетить, что дополнительное расширение достаточно сильно увеличивает размеры расширенной части таблицы, поэтому стоит предел в 2 дополнительных расширения.

**counter** - число символов, на которое происходит дополнительное расширение(изначально равно двум)

Опять же, при дополнительном расширении строчки в расширенной части могут дублироваться. Для решения этой проблемы используется функция **make_checked_extension!(table, pref, n, start)**, которая исключает дублирование.

Реализация проверки на необходимость в дополнительном расширении:
```
    while requirement_for_extra && counter < 4
        for i in start_extra:(start_extension - 1)
            make_checked_extension!(table, table[i][1], counter, i)
        end
        
        _, start_extension = solve_incompleteness!(table, start_extra, start_extension, counter)
        counter += 1
    end
    
    start_extra = start_extension
```
# Работа с оптимизацией
Для ускорения работы программы можно менять два следующий параметра:
  1. Ограничение на дополнительное расширение (counter < 4)
  2. Разницу между числом имеющихся классов и числом ветвлений (requirement_for_extra = 5 * (start_extension - 2) < num_of_vertices)
