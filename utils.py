import json


def split_file(ipath, n):
    """Divide array into chunks of size n.

    Parameters
    ---------- array : list
        Long list.
    n : int
        Size of each chunk.

    """

    with open(ipath, 'r') as ifp:
        count = sum(1 for doc in ifp)
    for low_bound in range(0, count, n):
        high_bound, docs = low_bound + n, []
        with open(ipath, 'r') as ifp:
            for ix, doc in enumerate(ifp):
                if ix < low_bound:
                    continue
                if ix >= high_bound:
                    break
                docs.append(json.loads(doc))
        yield docs
