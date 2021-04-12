from collections import Counter, defaultdict

import logging

logger = logging.getLogger(__name__)


def most_repeated_values(query_list):
    values = []
    for k in query_list[0].keys():
        val, _ = (Counter(d[k] for d in query_list).most_common(1)[0])
        values.append(val)

    return values

def average_values(query_list):
    values = []
    int = defaultdict(list)

    for subdict in query_list:
        for k, v in subdict.items():
            int[k].append(v)

    for val in int.values():
        values.append(round(sum(val)/len(val), 2))

    return values