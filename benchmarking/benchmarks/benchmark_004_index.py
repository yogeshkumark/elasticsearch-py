# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

# Licensed to Elasticsearch B.V. under one or more agreements.
# Elasticsearch B.V. licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information.

import random
import functools
from benchmarking.lib import benchmarks, Action, RunnerConfig


@functools.lru_cache()
def small_doc(data_path):
    with open(data_path / "small/document.json", mode="rb") as f:
        return f.read()


def setup_func(_: int, config: RunnerConfig) -> None:
    config.target_es.indices.delete(index="test-bench-index", ignore=404)
    config.target_es.indices.create(index="test-bench-index")
    config.target_es.cluster.health(wait_for_status="yellow")


def run_func(n: int, config: RunnerConfig) -> None:
    resp = config.target_es.index(
        index="test-bench-index",
        id="%d-%d" % (n, random.randint(1, 10000)),
        body=small_doc(config.data_path),
    )
    assert resp["result"] == "created", resp["result"]


benchmarks.register(
    Action(
        action="index",
        category="core",
        run_func=run_func,
        setup_func=setup_func,
        num_warmups=100,
        num_repetitions=10000,
    )
)
