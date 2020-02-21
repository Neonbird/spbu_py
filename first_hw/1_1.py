from string import ascii_uppercase

num_to_let = {}
num = 10
for lett in ascii_uppercase:
    num_to_let[lett] = num
    num += 1

let_to_num = {}
num = 10
for lett in ascii_uppercase:
    let_to_num[num] = lett
    num += 1


def base_to_ten(number, base):
    number = list(number)
    if base > 10:
        for index, numeral in enumerate(number):
            if numeral in num_to_let.keys():
                number[index] = num_to_let[numeral]
    number = [int(x) for x in number]
    num_base_ten = 0
    for index, numeral in enumerate(number[::-1]):
        num_base_ten += int(numeral) * (base ** index)
    return num_base_ten


def ten_to_result_base(number_in_ten, base_of_res, num_res_base=None):
    if num_res_base is None:
        num_res_base = []
    remainder = number_in_ten % base_of_res
    quotient = number_in_ten // base_of_res
    num_res_base.append(remainder)
    if quotient <= base_of_res - 1:
        num_res_base.append(quotient)
    else:
        ten_to_result_base(quotient, base_of_res, num_res_base)
    if base_of_res > 10:
        for index, numeral in enumerate(num_res_base):
            if numeral in let_to_num.keys():
                num_res_base[index] = let_to_num[numeral]
    return num_res_base[::-1]


base, first_num, second_num, base_result = \
    int(input('base: ')), input("first number: "), \
    input("second number: "), int(input('base of resulting number: '))

sum_in_ten = base_to_ten(first_num, base) + base_to_ten(second_num, base)
print(''.join([str(x) for x in ten_to_result_base(sum_in_ten, base_result)]))
