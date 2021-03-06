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

from surveil.api.datamodel.config import timeperiod
from surveil.api.handlers import mongo_object_handler


class TimePeriodHandler(mongo_object_handler.MongoObjectHandler):
    """Fulfills a request on the Time Period resource."""

    def __init__(self, *args, **kwargs):
        super(TimePeriodHandler, self).__init__(
            'timeperiods',
            'timeperiod_name',
            timeperiod.TimePeriod,
            *args,
            **kwargs
        )
