#!/usr/bin/env python

from collections import namedtuple

PostCode = namedtuple("PostCode", ["post_code", "position"])

Position = namedtuple("Position", ["longitude", "latitude"])

ItsuBranch = namedtuple("ItsuBranch", ["name", "position", "address", "post_code", "weekday", "saturday", "sunday"])
