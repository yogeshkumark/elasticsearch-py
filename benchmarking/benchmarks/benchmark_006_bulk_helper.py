# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import json
from elasticsearch.helpers import bulk
from benchmarking.lib import benchmarks, Action, RunnerConfig


def setup_func(_: int, config: RunnerConfig):
    config.target_es.indices.delete(index="test-bench-bulk-helper", ignore=404)
    config.target_es.indices.create(
        index="test-bench-bulk-helper",
        wait_for_active_shards=1,
        body={"settings": {"number_of_shards": 3, "refresh_interval": "5s"}},
    )
    config.target_es.cluster.health(wait_for_status="yellow")


def run_func(_: int, config: RunnerConfig) -> None:
    with open(config.data_path / "small/document.json", mode="r") as f:
        doc = json.loads(f.read().replace("\n", ""))
    doc["_index"] = "test-bench-bulk-helper"

    def generator():
        for _ in range(1000000):
            yield doc

    bulk(
        client=config.target_es,
        actions=generator()
    )


benchmarks.register(
    Action(
        action="bulk-helper",
        category="helpers",
        run_func=run_func,
        setup_func=setup_func,
        num_warmups=1,
        num_repetitions=10,
        num_operations=1000000,
    )
)
