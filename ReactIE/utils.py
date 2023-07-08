def remove_duplicate_dicts(dict_list):
    """
    This function takes a list of dictionaries as input and returns a new list with duplicate dictionaries removed.
    """
    unique_dicts = {str(d): d for d in dict_list}
    return list(unique_dicts.values())

def merge_dicts_on_all_keys_except_product(dict_list):
    """
    This function takes a list of dictionaries as input and returns a new list with dictionaries merged
    based on the condition that all keys, except the "product" key, have the same values.
    """
    merged_dicts = []
    for dict1 in dict_list:
        merged = False
        for dict2 in merged_dicts:
            # Check if both dictionaries have the same set of keys
            if set(dict1.keys()) == set(dict2.keys()):
                # Check if all keys except "product" have the same values
                if all(dict1[k] == dict2[k] for k in dict1.keys() if k != "product"):
                    # Merge the dictionaries by concatenating the "product" values
                    dict2["product"] = dict1['product'] + ', ' + dict2['product']
                    merged = True
                    break

        if not merged:
            merged_dicts.append(dict1)

    return merged_dicts

def remove_duplicates_except_text_key(dict_list):
    """
    This function takes a list of dictionaries as input and returns a new list with duplicate values removed for all keys except the "text" key.
    """
    for d in dict_list:
        for key, value in d.items():
            if key != "text":
                unique_values = set(value.split(", "))
                d[key] = ", ".join(unique_values)
    return dict_list

def filter_dict_list(dict_list):
    """
    This function takes a list of dictionaries as input and returns a new list with dictionaries filtered
    based on the following conditions:
    1. Remove dictionaries with less than 4 keys.
    2. If a dictionary has exactly 3 keys and they are "text", "product" and "reactants", keep it.
    3. Remove chemical reactions without "reactants".
    """
    filtered_list = []
    for d in dict_list:
        if len(d.keys()) > 3 or (len(d.keys()) == 3 and set(d.keys()) == {'reactants', 'product', 'text'}):
            if 'reactants' in d:
                filtered_list.append(d)
    return filtered_list

def reorder_reactions(reactions):
    key_order = ['product', 'reactants', 'reaction type', 'catalyst', 'solvent', 'temperature', 'time', 'yield', 'text']
    return [{key: d[key] for key in key_order if key in d} for d in reactions]

def process_reactions(reactions):
    reactions = remove_duplicate_dicts(reactions)
    reactions = merge_dicts_on_all_keys_except_product(reactions)
    reactions = remove_duplicates_except_text_key(reactions)
    reactions = filter_dict_list(reactions)
    reactions = reorder_reactions(reactions)
    return reactions


