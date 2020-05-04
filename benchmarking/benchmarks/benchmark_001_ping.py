from benchmarking.lib import benchmarks, Operation, RunnerConfig


def run_func(_: int, config: RunnerConfig) -> None:
    config.target_es.ping()


benchmarks.register(
    Operation(
        action="ping",
        category="core",
        run_func=run_func,
        num_repetitions=10000
    )
)
