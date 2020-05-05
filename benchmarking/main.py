# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import sys
from pathlib import Path
import platform

sys.path.append(str(Path(__file__).absolute().parent.parent))

import logging
import os
from elasticsearch import Elasticsearch, __versionstr__
from benchmarking.lib import benchmarks, Runner, RunnerConfig, Service


def main():
    envvars = {
        "BUILD_ID",
        "DATA_SOURCE",
        "CLIENT_BRANCH",
        "CLIENT_COMMIT",
        "CLIENT_BENCHMARK_ENVIRONMENT",
        "ELASTICSEARCH_TARGET_URL",
        "ELASTICSEARCH_REPORT_URL",
        "TARGET_SERVICE_TYPE",
        "TARGET_SERVICE_NAME",
        "TARGET_SERVICE_VERSION",
        "TARGET_SERVICE_OS_FAMILY",
    }
    config = {k: os.getenv(k, "") for k in envvars}
    if any(v == "" for v in config.values()):
        raise ValueError(
            f"Required environment variables empty: "
            f"{', '.join(k for k, v in config.items() if v == '')}"
        )

    if not os.path.exists(config["DATA_SOURCE"]):
        raise ValueError(f"Data source at {config['DATA_SOURCE']!r} does not exist")

    target_es = Elasticsearch(config["ELASTICSEARCH_TARGET_URL"])
    report_es = Elasticsearch(config["ELASTICSEARCH_REPORT_URL"])

    if os.getenv("DEBUG", ""):
        logger = logging.getLogger("elasticsearch")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

    runner_config = RunnerConfig(
        target_es=target_es,
        report_es=report_es,
        build_id=config["BUILD_ID"],
        category=os.getenv("CLIENT_BENCHMARK_CATEGORY", ""),
        environment=config["CLIENT_BENCHMARK_ENVIRONMENT"],
        client=Service(
            type="client",
            name="elasticsearch-py",
            version=__versionstr__,
            os_family=platform.system().lower(),
            git_branch=config["CLIENT_BRANCH"],
            git_commit=config["CLIENT_COMMIT"],
        ),
        target_service=Service(
            type=config["TARGET_SERVICE_TYPE"],
            name=config["TARGET_SERVICE_NAME"],
            version=config["TARGET_SERVICE_VERSION"],
            os_family=config["TARGET_SERVICE_OS_FAMILY"],
            git_branch=config.get("TARGET_SERVICE_GIT_BRANCH"),
            git_commit=config.get("TARGET_SERVICE_GIT_COMMIT"),
        ),
        data_path=Path(config["DATA_SOURCE"]).absolute(),
    )
    runner = Runner(runner_config)

    # Load all the benchmarks from 'benchmarks/'
    base_path = Path(__file__).absolute().parent / "benchmarks"
    sys.path.append(str(base_path))
    for filename in base_path.iterdir():
        if filename.name.endswith(".py") and filename.name != "__init__.py":
            __import__(filename.name[:-3])

    for operation in benchmarks.operations:
        if "FILTER" in os.environ and operation.action not in os.environ["FILTER"]:
            continue
        runner.run(operation)


if __name__ == "__main__":
    main()
