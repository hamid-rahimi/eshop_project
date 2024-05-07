
def convert_to_group_list(main_list : list, group_length : int = 4):
    grouped_list = []
    for i in range(0, len(main_list), group_length):
        grouped_list.append(main_list[i : i + group_length])
    return grouped_list
