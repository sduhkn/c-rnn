#!/usr/bin/env python
from __future__ import division
from __future__ import print_function

import collections
import numpy as np

from math import ceil


class Dataset(object):

    def __init__(self, nb_users, nb_items, seq_dict):
        self._seq_dict = seq_dict
        self._nb_users = nb_users
        self._nb_items = nb_items

    @property
    def nb_users(self):
        return self._nb_users

    @property
    def nb_items(self):
        return self._nb_items

    def iterate(self, uid, subseq_len):
        seq = np.asarray(self._seq_dict[uid])
        for i in range(0, len(seq) - 1, subseq_len):
            targets = seq[np.newaxis,i+1:i+1+subseq_len]
            n = targets.shape[1]
            inputs = seq[np.newaxis,i:i+n]
            yield (inputs, targets)

    @classmethod
    def from_path(cls, path):
        data = collections.defaultdict(list)
        nb_users = 0
        nb_items = 0
        with open(path) as f:
            for line in f:
                u, i, t = map(int, line.strip().split())
                nb_users = max(u + 1, nb_users)  # Users are numbered 0 -> N-1.
                nb_items = max(i + 1, nb_items)  # Items are numbered 0 -> M-1.
                data[u].append((t, i))
        sequence = dict()
        for user, pairs in data.items():
            sequence[user] = tuple(i for t, i in sorted(pairs))
        return cls(nb_users, nb_items, sequence)
