#!/bin/env python2.7
#
# Copyright 2015 Peter Griess
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.

import argparse
import datetime
import csv
from foodscores.inspection import Inspection
import logging
import os.path
import sys


def main(argv):
    ap = argparse.ArgumentParser(
        description='''
Given CSV files from download-scores, emit a CSV file that is the union of all
inputs. Writes outout CSV to stdout.
''')
    ap.add_argument(
        'files', nargs='+', metavar='file', default=[],
        help='CSV file to combine')
    ap.add_argument(
        '-v', '--verbose', action='count', dest='verbosity', default=0,
        help='increase global logging verbosity; can be used multiple times')

    args = ap.parse_args()

    logging.basicConfig(
            level=logging.ERROR - args.verbosity * 10,
            style='{',
            format='{}: {{message}}'.format(ap.prog))

    inspections = set()
    for cfp in args.files:
        with open(cfp) as cf:
            cr = csv.DictReader(cf)
            inspections |= set(Inspection.from_dict(r) for r in cr)

    cw = csv.DictWriter(
            sys.stdout,
            fieldnames=Inspection.FIELDNAMES)
    cw.writeheader()
    cw.writerows(r.to_dict() for r in sorted(inspections))


if __name__ == '__main__':
    main(sys.argv)
