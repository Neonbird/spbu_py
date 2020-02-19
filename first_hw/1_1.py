def base_to_ten(number, base):
    number = list(number)
    if base == 16:
        sixteen_to_ten = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
        for index, numeral in enumerate(number):
            if numeral in sixteen_to_ten.keys():
                number[index] = sixteen_to_ten[numeral]
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
    if base_of_res == 16:
        ten_to_sixteen = {10:"A", 11:"B", 12:"C", 13:"D", 14:"E", 15:"F"}
        for index, numeral in enumerate(num_res_base):
            if numeral in ten_to_sixteen.keys():
                num_res_base[index] = ten_to_sixteen[numeral]
    return num_res_base[::-1]


base, first_num, second_num, base_result = \
    int(input('base: ')), input("first number: "), \
    input("second number: "), int(input('base of resulting number: '))

sum_in_ten = base_to_ten(first_num, base) + base_to_ten(second_num, base)
print(''.join([str(x) for x in ten_to_result_base(sum_in_ten, base_result)]))
