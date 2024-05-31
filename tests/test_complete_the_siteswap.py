from source.complete_the_siteswap import complete

def test_one_missing_throw() -> None:
    partial = [4, "?", 3]
    assert complete(partial, [1, 2, 3, 4, 5]) == [[4, 2, 3], [4, 5, 3]]

def test_two_throws_missing() -> None:
    partial = [5, "?", 7,  "?", 9]
    assert complete(partial, [5, 6, 7, 8, 9]) == [[5, 5, 7, 9, 9], [5, 6, 7, 8, 9]]