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

'''
Misc. utilities.
'''

import datetime

class Inspection(object):
    '''
    Object tracking a single inspection incident.
    '''

    def __init__(self, name, address, suite, zipcode, date, score,
                 inspection_type):
        self.name = name
        self.address = address
        self.suite = suite
        self.zipcode = zipcode
        self.date = date
        self.score = score
        self.inspection_type = inspection_type

    def to_dict(self):
        return {
                'name': self.name,
                'address_street': self.address,
                'address_suite': self.suite,
                'address_zip': self.zipcode,
                'inspection_date': self.date.strftime('%Y-%m-%d'),
                'inspection_score': self.score,
                'inspection_type': self.inspection_type,
        }

    @staticmethod
    def from_dict(d):
        return Inspection(
                name=d['name'],
                address=d['address_street'],
                suite=d['address_suite'],
                zipcode=d['address_zip'],
                date=datetime.datetime.strptime(d['inspection_date'], '%Y-%m-%d'),
                score=int(d['inspection_score']),
                inspection_type=d['inspection_type'])


    def __eq__(self, other):
        return self.name == other.name and \
                self.address == other.address and \
                self.suite == other.suite and \
                self.zipcode == other.zipcode and \
                self.date == other.date and \
                self.score == other.score and \
                self.inspection_type == other.inspection_type

    def __lt__(self, other):
        if self.date != other.date:
            return self.date < other.date

        if self.inspection_type != other.inspection_type:
            return self.inspection_type < other.inspection_type

        if self.score != other.score:
            return self.score < other.score

        if self.name != other.name:
            return self.name < other.name

        if self.address != other.address:
            return self.address < other.address

        if self.suite != other.suite:
            return self.suite < other.suite

        return self.zipcode < other.zipcode

    def __hash__(self):
        return hash(self.name) ^ \
                hash(self.address) ^ \
                hash(self.suite) ^ \
                hash(self.zipcode) ^ \
                hash(self.date) ^ \
                hash(self.score) ^ \
                hash(self.inspection_type)
