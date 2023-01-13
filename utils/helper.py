
def pairwise(iterable):
    iterable = iter(iterable)
    while True:
        try:
            yield next(iterable), next(iterable)
        except StopIteration:
            # no more elements in the iterator
            return