# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from benchmarking.lib import benchmarks, Action, RunnerConfig


def setup_func(_: int, config: RunnerConfig):
    config.target_es.indices.delete(index="test-bench-bulk", ignore=404)
    config.target_es.indices.create(
        index="test-bench-bulk",
        body={"settings": {"number_of_shards": 3, "refresh_interval": "5s"}},
    )
    config.target_es.cluster.health(wait_for_status="yellow")


def run_func(_: int, config: RunnerConfig) -> None:
    with open(config.data_path / "small/document.json", mode="r") as f:
        doc = f.read().replace("\n", "")

    def generator():
        for _ in range(10000):
            yield '{"index":{}}'
            yield doc

    body = "\n".join(generator())
    config.target_es.bulk(index="test-bench-bulk", body=body)


benchmarks.register(
    Action(
        action="bulk",
        category="core",
        run_func=run_func,
        setup_func=setup_func,
        num_warmups=10,
        num_repetitions=1000,
        num_operations=10000,
    )
)
