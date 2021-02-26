from itertools import compress


def bool_code(number):
    b = list()
    while number != 0:
        if number % 2 == 1:
            b.append(True)
        else:
            b.append(False)
        number >>= 1
    return b


def bit_not(n, num_bits):
    return (1 << num_bits) - 1 - n


def translate_code(items, mask):
    return ' '.join(list(compress(items, bool_code(mask))))


def print_closed_frequent_itemsets(closed_frequent_itemsets, l1):
    for itemset in closed_frequent_itemsets:
        print(translate_code(l1, itemset), ' #SUP:', closed_frequent_itemsets[itemset])


def bit_map_code(transaction, f_1, l_1):
    bc = 0
    for item in transaction:
        if item in f_1:
            f_1[item] += 1
        else:
            f_1[item] = 1
            l_1.append(item)

        bc += 2 ** l_1.index(item)

    # return bc, transaction.__len__(), f_1, l_1
    return bc, f_1, l_1
