# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from benchmarking.lib import benchmarks, Operation, RunnerConfig


def setup_func(_: int, config: RunnerConfig) -> None:
    config.target_es.indices.delete(index="test-bench-get", ignore=404)
    config.target_es.index(index="test-bench-get", id="1", body={"title": "Test"})
    config.target_es.cluster.health(wait_for_status="yellow")
    config.target_es.indices.refresh(index="test-bench-get")


def run_func(_: int, config: RunnerConfig) -> None:
    config.target_es.get(index="test-bench-get", id="1")


benchmarks.register(
    Operation(
        action="get",
        category="core",
        run_func=run_func,
        setup_func=setup_func,
        num_repetitions=10000,
    )
)
