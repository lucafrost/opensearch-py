# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from ..client.utils import NamespacedClient, _make_path, query_params


class KnnClient(NamespacedClient):
    """
    Client for k-Nearest Neighbor (k-NN) API abstractions, used to
    simplify k-NN queries and call APIs for the k-NN plugin.

    OS Docs: https://opensearch.org/docs/latest/search-plugins/knn/api/
    GitHub Issue: https://github.com/opensearch-project/opensearch-py/issues/300 
    """

    @query_params()
    def approx(self, index, field, vector, size=10, params=None, headers=None):
        """
        Perform approximate k-NN searching on an index.
        Docs: https://opensearch.org/docs/latest/search-plugins/knn/approximate-knn/

        :arg index: 
        :arg field: 
        :arg vector:
        :arg size: 
        """
        body = {
            "size", size,
            "query": {
                "knn": {
                    field: {
                        "vector": vector,
                        "k": size
                    }
                }
            }
        }
        return self.transport.perform_request(
            "POST",
            _make_path(index, "_search"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def exact(self, monitor_id, params=None, headers=None):
        """
        Perform exact k-NN searching on an index.
        Docs: https://opensearch.org/docs/latest/search-plugins/knn/knn-score-script/

        :arg monitor_id: The id of the monitor we are trying to fetch
        """

        # {
        # "size": 4,
        # "query": {
        # "script_score": {
        #     "query": {
        #     "match_all": {}
        #     },
        #     "script": {
        #     "source": "knn_score",
        #     "lang": "knn",
        #     "params": {
        #         "field": "my_vector2",
        #         "query_value": [2.0, 3.0, 5.0, 6.0],
        #         "space_type": "cosinesimil"
        #     }
        #     }
        # }
        # }
        # }
        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_alerting", "monitors", monitor_id),
            params=params,
            headers=headers,
        )

    @query_params("dryrun")
    def run_monitor(self, monitor_id, params=None, headers=None):
        """
        Runs/Executes a specific monitor.

        :arg monitor_id: The id of the monitor we are trying to execute
        :arg dryrun: Shows the results of a run without actions sending any message
        """
        return self.transport.perform_request(
            "POST",
            _make_path("_plugins", "_alerting", "monitors", monitor_id, "_execute"),
            params=params,
            headers=headers,
        )

    @query_params()
    def create_monitor(self, body=None, params=None, headers=None):
        """
        Creates a monitor with inputs, triggers, and actions.

        :arg body: The configuration for the monitor (`inputs`, `triggers`, and `actions`)
        """
        return self.transport.perform_request(
            "POST",
            _make_path("_plugins", "_alerting", "monitors"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def update_monitor(self, monitor_id, body=None, params=None, headers=None):
        """
        Updates a monitor's inputs, triggers, and actions.

        :arg monitor_id: The id of the monitor we are trying to update
        :arg body: The configuration for the monitor (`inputs`, `triggers`, and `actions`)
        """
        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_alerting", "monitors", monitor_id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def delete_monitor(self, monitor_id, params=None, headers=None):
        """
        Deletes a specific monitor.

        :arg monitor_id: The id of the monitor we are trying to delete
        """
        return self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_alerting", "monitors", monitor_id),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_destination(self, destination_id=None, params=None, headers=None):
        """
        Returns the details of a specific destination.

        :arg destination_id: The id of the destination we are trying to fetch. If None, returns all destinations
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_alerting", "destinations", destination_id)
            if destination_id
            else _make_path("_plugins", "_alerting", "destinations"),
            params=params,
            headers=headers,
        )

    @query_params()
    def create_destination(self, body=None, params=None, headers=None):
        """
        Creates a destination for slack, mail, or custom-webhook.

        :arg body: The configuration for the destination
        """
        return self.transport.perform_request(
            "POST",
            _make_path("_plugins", "_alerting", "destinations"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def update_destination(self, destination_id, body=None, params=None, headers=None):
        """
        Updates a destination's inputs, triggers, and actions.

        :arg destination_id: The id of the destination we are trying to update
        :arg body: The configuration for the destination
        """
        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_alerting", "destinations", destination_id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def delete_destination(self, destination_id, params=None, headers=None):
        """
        Deletes a specific destination.

        :arg destination_id: The id of the destination we are trying to delete
        """
        return self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_alerting", "destinations", destination_id),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_alerts(self, params=None, headers=None):
        """
        Returns all alerts.

        """
        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_alerting", "monitors", "alerts"),
            params=params,
            headers=headers,
        )

    @query_params()
    def acknowledge_alert(self, monitor_id, body=None, params=None, headers=None):
        """
        Acknowledges an alert.

        :arg monitor_id: The id of the monitor, the alert belongs to
        :arg body: The alerts to be acknowledged
        """
        return self.transport.perform_request(
            "POST",
            _make_path(
                "_plugins",
                "_alerting",
                "monitors",
                monitor_id,
                "_acknowledge",
                "alerts",
            ),
            params=params,
            headers=headers,
            body=body,
        )
