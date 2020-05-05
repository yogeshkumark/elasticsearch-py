# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from benchmarking.lib import benchmarks, Operation, RunnerConfig


def run_func(_: int, config: RunnerConfig) -> None:
    config.target_es.ping()


benchmarks.register(
    Operation(action="ping", category="core", run_func=run_func, num_repetitions=10000)
)
