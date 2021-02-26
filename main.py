from utils.dataset.transactional.spmf import *
from anytree import Node, RenderTree

b_i = set()
vertical_view = VerticalView()
horizontal_view = HorizontalView()


def calc_topological_basis(dataset, min_sup):
    global horizontal_view, vertical_view

    vertical_view = VerticalView()
    horizontal_view = HorizontalView()

    for transaction_id, transaction in enumerate(Dataset(dataset).transactions()):
        horizontal_view.add_transaction(transaction)
        vertical_view.add_transaction(transaction, transaction_id)

    bi = list()

    for item in vertical_view.items.keys():
        c_i = set()
        if vertical_view.items[item].__len__() >= min_sup:
            c_i = set(horizontal_view.include_item_set(vertical_view.items[item][0]))
            for j in range(1, vertical_view.items[item].__len__()):
                c_i.intersection(set(horizontal_view.include_item_set(vertical_view.items[item][j])))

            bi.append(c_i)

    return sorted(bi, key=len)


def construct_tt_tree(dataset, min_sup):
    global b_i
    b_i = calc_topological_basis(dataset, min_sup)
    tree = Node([None, horizontal_view.transactions])
    for j, topological_basis in enumerate(b_i):
        Node([set(list(b_i)[j]), horizontal_view.include_item_set(list(b_i)[j])], parent=tree)
        tt_tree_extend(set(list(b_i)[j]), set(list(b_i)[j]), j, tree, min_sup)
    return tree


def tt_tree_extend(item_set: set, transactions: set, j, parent, min_sup):
    for k in range(j, b_i.__len__()):
        if (not set(list(b_i)[k]).issubset(item_set)) and len(
                set(horizontal_view.include_item_set(list(item_set))).intersection(
                    set(horizontal_view.include_item_set(list(b_i)[k])))) >= min_sup:
            item_set.union(set(list(b_i)[k]))
            transactions = set(horizontal_view.include_item_set(list(item_set))).intersection(
                set(horizontal_view.include_item_set(list(b_i)[k])))
            Node([item_set, horizontal_view.include_item_set(item_set)], parent=parent)
            tt_tree_extend(item_set, transactions, k, parent, min_sup)


def hash_function(item_set):
    item_set_hash = []
    for transaction_id in horizontal_view.include_item_set(item_set):
        item_set_hash.append(list(horizontal_view.transactions)[transaction_id])
    return item_set_hash


def obtain_fcis(root_node):
    c = []
    hash_table = list()
    for pre, fill, node in RenderTree(root_node):
        hash_table.append([[node.value, horizontal_view.include_item_set(node.value)], hash_function(node.value)])

    for pre, fill, node in RenderTree(root_node):
        h_i = hash_function(node.value)
        for hash in hash_table:
            if set(hash[0]).issubset(h_i) and horizontal_view.include_item_set(
                    hash[1]) == horizontal_view.include_item_set(node.value):
                c.append(node.value)

    return c


def tt_miner(dataset, min_sup):
    c = list()
    b_i = calc_topological_basis(dataset, min_sup)
    tt_miner_extend(dataset, [], horizontal_view.transactions, c, b_i)
    return c


def tt_miner_extend(dataset, current_frequent_closed_itemset, transaction_including, c, b_i):
    c.append(current_frequent_closed_itemset)
    for i in range(len(b_i)):
        current_frequent_closed_itemset = set(current_frequent_closed_itemset).union(set(list(b_i)[i]))
        set(horizontal_view.include_item_set(current_frequent_closed_itemset)).intersection(
            set(horizontal_view.include_item_set(list(b_i)[i])))
        tt_miner_extend(dataset, current_frequent_closed_itemset,
                        horizontal_view.include_item_set(current_frequent_closed_itemset), c, b_i)
    return
