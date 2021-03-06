# Copyright 2014 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from surveil.api.datamodel.status.metrics import live_metric
from surveil.api.handlers import handler
from surveil.api.handlers.status.metrics import influxdb_time_query


class MetricHandler(handler.Handler):
    """Fulfills a request on the metrics."""

    def get(self, host_name, metric_name=None, service_description=None):
        """Return metrics name if param metric_name is null,

         else , return the last metric.
        """
        metrics = []
        cli = self.request.influxdb_client
        if metric_name is None:
            if service_description is None:
                query = ("SHOW measurements WHERE host_name='%s' "
                         "AND service_description=''"
                         % host_name)
            else:
                query = ("SHOW measurements WHERE host_name='%s' "
                         "AND service_description='%s'"
                         % (host_name, service_description))
        else:
            if service_description is None:
                query = ("SELECT * FROM metric_%s "
                         "WHERE host_name= '%s' "
                         "GROUP BY service_description "
                         "ORDER BY time DESC "
                         "LIMIT 1"
                         % (metric_name, host_name))
            else:
                query = ("SELECT * FROM metric_%s "
                         "WHERE host_name= '%s' "
                         "AND service_description= '%s'"
                         "ORDER BY time DESC "
                         "LIMIT 1"
                         % (metric_name, host_name, service_description))

        response = cli.query(query)

        if metric_name is None:
            metric_dicts = []

            for item in response[None]:
                metric_dict = self._metric_dict_from_influx_item(item)
                if metric_dict is not None:
                    metric_dicts.append(metric_dict)

            for metric_dict in metric_dicts:
                metric = live_metric.LiveMetric(**metric_dict)
                metrics.append(metric)

        else:
            metrics = live_metric.LiveMetric(**self.
                                             _metric_dict_from_influx_item(
                                                 next(response.items()[0][1]),
                                                 metric_name))

        return metrics

    def get_all(self, metric_name, time_delta, host_name=None,
                service_description=None):
        """Return all metrics."""

        cli = self.request.influxdb_client
        query = influxdb_time_query.build_influxdb_query(
            metric_name,
            time_delta,
            host_name,
            service_description
        )
        response = cli.query(query)

        metric_dicts = []

        for item in response[None]:
            metric_dict = self._metric_dict_from_influx_item(item, metric_name)
            metric_dicts.append(metric_dict)

        metrics = []
        for metric_dict in metric_dicts:
            metric = live_metric.LiveMetric(**metric_dict)
            metrics.append(metric)

        return metrics

    def _metric_dict_from_influx_item(self, item, metric_name=None):

        if metric_name is None:
            metric_dict = None
            mappings = [('name', 'metric_name', str), ]
        else:
            metric_dict = {"metric_name": str(metric_name)}
            mappings = [
                ('min', str),
                ('max', str),
                ('critical', str),
                ('warning', str),
                ('value', str),
                ('unit', str),
            ]

        for field in mappings:
            value = item.get(field[0], None)
            if value is not None:
                if field[0] == 'name':
                    if value.startswith('metric_'):
                        metric_dict = {}
                        metric_dict[field[1]] = field[2](value[7:])
                else:
                    metric_dict[field[0]] = field[1](value)

        return metric_dict