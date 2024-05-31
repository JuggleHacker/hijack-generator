def state(siteswap):
    """ Takes a list of integers, represting the siteswap being juggled and returns the state """

    # Look backwards for what has been thrown, and where it is hitting.
    # How many throws do you need to look back? At most the highest throw
    highest_throw = max(siteswap)
    period = len(siteswap)
    i = 1
    landing_times = []
    while i <= highest_throw:
        j = (i % period)
        if siteswap[-j] != 0:
            if -i + siteswap[-j] >= 0: # object still has to land!
                landing_times.append(-i + siteswap[-j])
        i += 1

    latest_landing_object = max(landing_times)
    state = [0] * (latest_landing_object + 1)
    for landing_time in landing_times:
        state[landing_time] += 1
    return state

def make_a_throw(throw, state):
    """ Returns the new state after making the given throw """
    if state[0] == 0:
        if throw != 0:
            return False
        else:
            return state[1:]
    else: # we have an object to make a throw with!
        new_state = state.copy()
        if throw >= len(state):
            new_state += [0] * (throw - len(state) + 1)
            new_state[throw] = 1
        else:
            new_state[throw] += 1
    return new_state[1:]
