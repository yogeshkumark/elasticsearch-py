from benchmarking.lib import benchmarks, Operation, RunnerConfig


def setup_func(_: int, config: RunnerConfig):
    config.target_es.delete(index="test-bench-bulk", ignore=404)
    config.target_es.create(index="test-bench-bulk", body={"settings": {"number_of_shards": 3, "refresh_interval": "5s"}})
    config.target_es.cluster.health(wait_for_status="yellow")


def run_func(_: int, config: RunnerConfig) -> None:
    with open(config.data_path / "small/document.json", mode="r") as f:
        doc = f.read().rstrip("\r\n")
    body = ['{"index":{}}', doc]
    config.target_es.bulk(index="test-bench-bulk", body=body * 10000)


benchmarks.register(
    Operation(
        action="bulk",
        category="core",
        run_func=run_func,
        setup_func=setup_func,
        num_warmups=10,
        num_repetitions=1000,
        num_operations=10000,
    )
)
