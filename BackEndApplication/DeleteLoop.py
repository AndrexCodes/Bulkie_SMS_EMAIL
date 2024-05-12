def deleteGroup(mass_data, del_groups):
    mass_data = mass_data
    count = 0
    for x in mass_data:
        if x["group_name"] in del_groups:
            mass_data.pop(count)
        count +=1
    return mass_data


def deleteContact():
    pass

def CorrectbyGroupNumber(db_data, new_data):
    if len(new_data) > len(db_data):
        new_groups = new_data[len(db_data):]
        for x in new_groups:
           db_data.append(x)
        return db_data
    else:
        return db_data
    
def CorrectbyGroupMagnitude(db_data, new_data):
    count = 0
    for x in db_data:
        for y in new_data:
            if x["group_name"] == y["group_name"]:
                array_of_dicts1 = x["phone_book"]
                array_of_dicts2 = y["phone_book"]
                # Convert each array of dicts to a set of frozensets to compare
                set_of_dicts1 = {frozenset(d.items()) for d in array_of_dicts1}
                set_of_dicts2 = {frozenset(d.items()) for d in array_of_dicts2}

                # Dictionaries in array_of_dicts1 but not in array_of_dicts2
                difference1 = [dict(fs) for fs in set_of_dicts1 - set_of_dicts2]

                # Dictionaries in array_of_dicts2 but not in array_of_dicts1
                difference2 = [dict(fs) for fs in set_of_dicts2 - set_of_dicts1]

                for a in difference2:
                    db_data[count]["phone_book"].append(a)
        count +=1
    return db_data

