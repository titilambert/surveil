# Copyright 2014 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy
import json

from surveil.tests.api import functionalTest


class TestRootController(functionalTest.FunctionalTest):

    def test_get_all_hosts(self):
        hosts = [
            {u"use": u"generic-host", u"contact_groups": u"admins",
             u"host_name": u"testhost1", u"address": u"www.google.ca"},
            {u"use": u"generic-host", u"contact_groups": u"admins",
             u"host_name": u"testhost2", u"address": u"www.google.ca"},
            {u"use": u"generic-host", u"contact_groups": u"admins",
             u"host_name": u"testhost3", u"address": u"www.google.ca"}
        ]
        self.mongoconnection.shinken.hosts.insert(copy.deepcopy(hosts))

        response = self.app.get('/v1/hosts')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            hosts
        )
        self.assertEqual(response.status_int, 200)

    def test_get_specific_host(self):
        hosts = [
            {u"use": u"generic-host", u"contact_groups": u"admins",
             u"host_name": u"testhost1", u"address": u"www.google.ca"},
            {u"use": u"generic-host", u"contact_groups": u"admins",
             u"host_name": u"testhost2", u"address": u"www.google.ca"},
            {u"use": u"generic-host", u"contact_groups": u"admins",
             u"host_name": u"testhost3", u"address": u"www.google.ca"}
        ]
        self.mongoconnection.shinken.hosts.insert(copy.deepcopy(hosts))

        response = self.app.get('/v1/hosts/testhost2')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            hosts[1]
        )
