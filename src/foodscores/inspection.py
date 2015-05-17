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
import hashlib

# XXX: Probably not ideal for this to define the CSV serialization field names,
#      but whatever.
class Inspection(object):
    '''
    Object tracking a single inspection incident.
    '''

    FIELDNAMES = [
            'name',
            'address_street',
            'address_suite',
            'address_zip',
            'inspection_date',
            'inspection_score',
            'inspection_type'
    ]

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
        d = {
                'name': self.name,
                'address_street': self.address,
                'address_suite': self.suite,
                'address_zip': self.zipcode,
                'inspection_date': self.date.strftime('%Y-%m-%d'),
                'inspection_score': self.score,
                'inspection_type': self.inspection_type,
        }
        for k, v in d.iteritems():
            if type(v) == unicode:
                v = v.encode('utf-8', 'replace')
            d[k] = v

        return d

    @staticmethod
    def from_dict(d):
        return Inspection(
                name=unicode(d['name'], 'utf-8', 'replace'),
                address=unicode(d['address_street'], 'utf-8', 'replace'),
                suite=unicode(d['address_suite'], 'utf-8', 'replace'),
                zipcode=unicode(d['address_zip'], 'utf-8', 'replace'),
                date=datetime.datetime.strptime(d['inspection_date'], '%Y-%m-%d'),
                score=int(d['inspection_score']),
                inspection_type=unicode(d['inspection_type'], 'utf-8', 'replace'))


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
        hd = hashlib.sha1(
                    u'{} {} {} {} {} {} {}'.format(
                        self.name, self.address, self.suite, self.zipcode,
                        self.date, self.score, self.inspection_type).
                            encode('utf-8')
        ).hexdigest()

        hv = 0
        while len(hd) > 0:
            i = int(hd[:16], 16)
            hv ^= i
            hd = hd[16:]

        return hv
