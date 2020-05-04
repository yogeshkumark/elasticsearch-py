import attr
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Callable, Any, Optional, List, Dict
from elasticsearch import Elasticsearch, TransportError, ElasticsearchException
from elasticsearch.helpers import bulk


@attr.s
class Service:
    type: str = attr.ib()
    name: str = attr.ib()
    version: str = attr.ib()
    git_branch: str = attr.ib()
    git_commit: str = attr.ib()


@attr.s
class RunnerConfig:
    target_es: Elasticsearch = attr.ib()
    report_es: Elasticsearch = attr.ib()
    build_id: str = attr.ib()
    category: str = attr.ib()
    environment: str = attr.ib()
    os_family: str = attr.ib()
    service: Service = attr.ib()
    data_path: Path = attr.ib()


@attr.s(slots=True)
class Operation:
    action: str = attr.ib()
    category: str = attr.ib()
    run_func: Callable[[int, RunnerConfig], None] = attr.ib()
    setup_func: Optional[Callable[[int, RunnerConfig], None]] = attr.ib(default=None)
    num_warmups: int = attr.ib(default=0)
    num_repetitions: int = attr.ib(default=1)
    num_operations: int = attr.ib(default=1)


@attr.s(slots=True)
class Stats:
    action: str = attr.ib()
    start_time: float = attr.ib()
    duration: float = attr.ib()
    outcome: str = attr.ib()
    status_code: Optional[int] = attr.ib()
    num_warmups: int = attr.ib()
    num_repetitions: int = attr.ib()
    num_operations: int = attr.ib()

    def to_json(self, config: RunnerConfig) -> Dict[str, Any]:
        return {
            "@timestamp": datetime.utcfromtimestamp(self.start_time).isoformat(),
            "labels": {
                "build_id": config.build_id,
                "client": "elasticsearch-py",
                "environment": config.environment,
            },
            "tags": ["bench", "elasticsearch-py"],
            "event": {
                "action": self.action,
                "duration": self.duration
            },
            "benchmark": {
                "build_id": config.build_id,
                "environment": config.environment,
                "category": config.category,
                "repetitions": self.num_repetitions,
                "operations": self.num_operations,
                "runner": {
                    "service": {
                        "type": "client",
                        "name": "elasticsearch-py",
                        "version": config.service.version,
                        "git_branch": config.service.git_branch,
                        "git_commit": config.service.git_commit,
                    },
                    "runtime": {
                        "name": "python",
                        "version": ".".join(str(x) for x in sys.version_info[:3])
                    }
                }
            }
        }


class Runner:
    def __init__(self, config: RunnerConfig):
        self.config = config

    def run(self, operation: Operation):
        if operation.setup_func:
            operation.setup_func(0, self.config)

        for _ in range(operation.num_warmups):
            operation.run_func(0, self.config)

        stats_to_publish = []
        for i in range(operation.num_repetitions):
            status_code = None
            outcome = "failure"
            start_time = time.time()
            try:
                operation.run_func(i, self.config)
                outcome = "success"
                status_code = 200
            # TransportError gives us a status code, still an error
            # but we potentially don't receive one with 'ElasticsearchException'.
            except TransportError as e:
                status_code = e.status_code
            except ElasticsearchException:
                pass
            finally:
                duration = time.time() - start_time
                stats_to_publish.append(Stats(
                    action=operation.action,
                    start_time=start_time,
                    duration=duration,
                    status_code=status_code,
                    outcome=outcome,
                    num_warmups=operation.num_warmups,
                    num_repetitions=operation.num_repetitions,
                    num_operations=operation.num_operations,
                ))

        self.publish_stats(stats_to_publish)

    def publish_stats(self, stats: List[Stats]) -> None:
        today = datetime.now()
        index_name = f"metrics-intake-{today.year}-{today.month}"

        def stream_actions():
            for stat in stats:
                yield {
                    "_index": index_name,
                    "doc": stat.to_json(self.config)
                }

        bulk(
            client=self.config.report_es,
            actions=stream_actions(),
        )


class Benchmarks:
    def __init__(self):
        self.operations = []

    def register(self, operation):
        self.operations.append(operation)


benchmarks = Benchmarks()
