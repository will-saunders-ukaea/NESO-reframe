site_configuration = {
    "systems": [
        {
            "name": "NESOReframe",
            "descr": "Runs NESO tests.",
            "hostnames": [
                "P0818",
            ],
            "modules_system": "tmod4",
            "max_local_jobs": 2,
            "stagedir": "/tmp/reframe",
            "partitions": [
                {
                    "max_jobs": 2,
                    "name": "default",
                    "descr": "Example partition",
                    "scheduler": "local",
                    "launcher": "mpirun",
                    "environs": [
                        "acpp_omp_accelerated",
                        "intel-oneapi",
                    ],
                    "prepare_cmds": [
                        "source ~/venvs/spack/v0.23",
                        "source /etc/profile.d/modules.sh",
                        "export CL_CONFIG_CPU_TARGET_ARCH=corei7-avx",
                        "export ACPP_ADAPTIVITY_LEVEL=0",
                        "export ACPP_APPDB_DIR=/dev/shm/acpp",
                        "export ACPP_RT_NO_JIT_CACHE_POPULATION=1",
                    ],
                }
            ],
        }
    ],
    "environments": [
        {
            "name": "acpp_omp_accelerated",
            "features": ["sycl"],
            "cc": "gcc",
            "cxx": "g++",
            "features": [],
            "extras": {
                "NUM_BUILD_WORKERS": 24,
                "NUM_MPI_RANKS": 8,
                "REFRAME_ENV": "acpp-omp-accelerated",
                "env_vars": {
                    "OMP_NUM_THREADS": 2,
                    "NESO_PARTICLES_DEVICE_AWARE_MPI": "ON",
                },
            },
            "modules": [],
        },
        {
            "name": "intel-oneapi",
            "features": ["sycl"],
            "cc": "icx",
            "cxx": "icpx",
            "features": [],
            "extras": {
                "NUM_BUILD_WORKERS": 24,
                "NUM_MPI_RANKS": 16,
                "REFRAME_ENV": "dpcpp",
                "env_vars": {
                    "OMP_NUM_THREADS": 2,
                    "I_MPI_PIN_DOMAIN": "2:scatter",
                    "NESO_PARTICLES_DEVICE_AWARE_MPI": "ON",
                },
            },
            "modules": [
                # fixes the sycl-ls not working with spack
                "intel-oneapi-compilers/2024.2.1-gcc-13.2.0-j6iedmj",
                "intel-oneapi-mpi/2021.14.0-oneapi-2024.2.1-pzfb27j",
            ],
        },
    ],
}
