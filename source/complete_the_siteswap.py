# If we have a partially complete siteswap, how can we fill in the gaps?
# Note, I will use "?" to denote a gap in the pattern

def valid_so_far(partial_siteswap):
    """ Takes a list of numbers and question markes as input.
    Returns False if there are collisions in the list already
    and returns True if the list can be completed to make a valid siteswap """
    period = len(partial_siteswap)
    landing_sites = set()
    for time, throw in enumerate(partial_siteswap):
        if throw == "?":
            continue
        else:
            landing_site = (time + throw) % period
            if landing_site in landing_sites:
                return False
            else:
                landing_sites.add(landing_site)
    return True


def ways_to_complete(partial_siteswap, list_of_throws, number_of_objects, solutions):

    if not valid_so_far(partial_siteswap):
        return None

    elif '?' not in partial_siteswap:
        if number_of_objects == None:
            solutions.append(partial_siteswap)
        elif int(sum(partial_siteswap)/len(partial_siteswap)) == number_of_objects:
            solutions.append(partial_siteswap)

    else:
        first_unknown_throw_index = partial_siteswap.index('?')
        for throw in list_of_throws:
            trial_siteswap = partial_siteswap.copy()
            trial_siteswap[first_unknown_throw_index] = throw
            ways_to_complete(trial_siteswap, list_of_throws, number_of_objects,solutions)
    return None

def complete(partial_siteswap, list_of_throws, number_of_objects=None):
    """ Takes in a partial siteswap and a list of throws.
    Returns the valid siteswaps which can be made by replacing the question marks
    in the partial siteswaps with throws from the list of throw.
    There is an optional parameter to filter the output to only include siteswaps
    with a certain number of objects.
    This does not currently filter the list so would output 423, 234 and 342.
    I may change this behaviour in the future."""

    solutions = []
    ways_to_complete(partial_siteswap, list_of_throws, number_of_objects, solutions)
    return solutions

def filter_rotations(list_of_siteswaps):
    """Takes in a list of siteswaps and removes any duplicates.
    The same siteswap can be written starting with different throws.
    For example: 441, 414 and 144 are all the same siteswap and this function
    would remove all apart from one of these from an input list."""
    filtered_list = []
    for list in list_of_siteswaps:
        list_to_be_added = True
        n = len(list)
        for i in range(n):
            if list[i:]+list[:i] in filtered_list:
                list_to_be_added = False
        if list_to_be_added:
            filtered_list.append(list)
    return filtered_list
