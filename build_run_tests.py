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


@rfm.simple_test
class NESOSpackEnvBuildRun(rfm.RegressionTest):
    valid_systems = ["NESOReframe"]
    valid_prog_environs = ["*"]
    sourcesdir = SOURCES_DIR
    build_system = "Spack"
    build_locally = False

    spack_exe = shutil.which("spack")
    spack_config_yaml = subprocess.check_output(
        (spack_exe + " config get config").split()
    ).decode(sys.stdout.encoding)
    spack_config = yaml.safe_load(spack_config_yaml)
    spack_install_tree = spack_config["config"]["install_tree"]["root"]

    @run_before("compile")
    def setup_build_system(self):
        # Add the existing spack directory as upstream to avoid rebuilding
        self.build_system.config_opts.append(
            f"upstreams:host:install_tree:{self.spack_install_tree}"
        )

        # define the spec reframe should add
        self.build_system.specs = [self.current_environ.extras["spec"]]

        # set the number of build workers
        self.build_system.max_concurrency = self.current_environ.extras[
            "NUM_BUILD_WORKERS"
        ]

    @sanity_function
    def validate_build(self):
        return True  # TODO
