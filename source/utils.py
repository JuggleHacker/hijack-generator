import programming
from collections import defaultdict
import pandas

def siteswap_in_list(list_of_siteswaps, siteswap):
    """ Takes a list of siteswaps, and a siteswap we are searching for.
    Returns the index if the siteswap is in the list, None otherwise.
    Note, if searching for 744 we have found it if 447 is in the list."""
    for i in range(len(siteswap)):
        if siteswap in list_of_siteswaps:
            return list_of_siteswaps.index(siteswap)
        else:
            siteswap = siteswap[1:] + siteswap[:1]
    return None

def find_network_of_hijacks(starting_pattern, permitted_throws, extra_passes=None, response_pass=None):

    transitions_found = 0
    patterns = [starting_pattern] # keep track of all patterns found
    new_patterns = [starting_pattern] # keep track of patterns found on latest loop
    keep_looping = True
    to_return = defaultdict(list)
    while keep_looping:
        newer_patterns = []
        for pattern in new_patterns:
            hijack = programming.generate_hijacks(pattern, permitted_throws, extra_passes, response_pass)
            hijack +=  programming.generate_hijacks(pattern[1:] + pattern[:1], permitted_throws, extra_passes, response_pass)
            for transition in hijack:
                if transition == None:
                    continue
                to_return["".join(str(throw) for throw in pattern)].append(transition[-1])
                transitions_found += 1
                index_of_pattern = siteswap_in_list(patterns, transition[1]) # None if not there
                if index_of_pattern == None:
                    newer_patterns.append(transition[1])
                    patterns.append(transition[1])
        if newer_patterns == []:
            keep_looping = False
        else:
            new_patterns = newer_patterns
    return to_return

if __name__ == "__main__":
    # hijacks = find_network_of_hijacks([9,2,6,9,2,6,8], [2,6,7,8,9])
    # print(len(hijacks))
    print(pandas.DataFrame())