import reframe as rfm
import reframe.utility.sanity as sn
import os
import shutil
import subprocess
import yaml
import sys

SOURCES_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "NESO-reframe-stage",
)


def make_path_to_env(reframe_env):
    return os.path.join(os.path.dirname(__file__), reframe_env)


class NESOTestsBuild(rfm.CompileOnlyRegressionTest):
    sourcesdir = SOURCES_DIR
    build_system = "CMake"
    build_locally = False
    executable = os.path.join("test", "unitTests")

    @run_before("compile")
    def prepare_build(self):
        self.build_system.max_concurrency = self.current_environ.extras[
            "NUM_BUILD_WORKERS"
        ]

        env_path = make_path_to_env(self.current_environ.extras["REFRAME_ENV"])
        self.env_vars["REFRAME_ENV"] = env_path
        self.build_system.make_opts += [
            "unitTests",
            "integrationTests",
            "solverIntegrationTests",
        ]

        # There must be a better way to do this that does not modify a
        # protected variable.
        self.current_environ._prepare_cmds += [
            f"echo 'activating env' {env_path}",
            f"spack env activate -d {env_path}",
            "spack install --only dependencies",
            "spack env view regenerate",
        ]

    @sanity_function
    def validate_build(self):
        return (
            os.path.exists(self.executable)
            and os.path.exists(os.path.join("test", "integrationTests"))
            and os.path.exists(
                os.path.join("solvers", "test", "solverIntegrationTests")
            )
        )


class NESOTest(rfm.RunOnlyRegressionTest):
    test_binaries = fixture(NESOTestsBuild, scope="environment")
    valid_systems = ["NESOReframe"]
    valid_prog_environs = ["*"]
    build_locally = False
    sourcesdir = SOURCES_DIR

    @run_before("run")
    def setup_omp_env(self):
        self.executable = os.path.join(
            self.test_binaries.stagedir,
            self.test_dir,
            self.test_name,
        )
        procinfo = self.current_partition.processor
        self.num_tasks = self.current_environ.extras["NUM_MPI_RANKS"]
        self.num_cpus_per_task = procinfo.num_cores
        self.env_vars = {}
        self.env_vars.update(self.current_environ.extras["env_vars"])

    @sanity_function
    def validate_solution(self):
        return (
            sn.assert_not_found(r"FAILED", self.stdout)
            and sn.assert_not_found(r"SKIPPED", self.stdout)
            and sn.assert_not_found(r"Assertion error", self.stderr)
        )


@rfm.simple_test
class NESOunitTestsTest(NESOTest):
    test_name = "unitTests"
    test_dir = "test"


@rfm.simple_test
class NESOintegrationTestsTest(NESOTest):
    test_name = "integrationTests"
    test_dir = "test"


@rfm.simple_test
class NESOsolverTestsTest(NESOTest):
    test_name = "solverIntegrationTests"
    test_dir = os.path.join("solvers", "test")
