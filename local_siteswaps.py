from complete_the_siteswap import valid_so_far
def is_valid_local(local_siteswap):
    global_siteswap = [0] * len(local_siteswap)
    for index, throw in enumerate(local_siteswap):
        global_siteswap[(2*index)%len(local_siteswap)] = throw
    return valid_so_far(global_siteswap), global_siteswap
