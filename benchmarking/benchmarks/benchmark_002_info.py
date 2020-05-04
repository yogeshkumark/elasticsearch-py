from benchmarking.lib import benchmarks, Operation, RunnerConfig


def run_func(_: int, config: RunnerConfig) -> None:
    config.target_es.info()


benchmarks.register(
    Operation(
        action="info",
        category="core",
        run_func=run_func,
        num_repetitions=10000
    )
)
