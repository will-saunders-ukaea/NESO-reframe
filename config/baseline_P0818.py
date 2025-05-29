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
                        "acpp_omp_library_only",
                    ],
                    "prepare_cmds": [
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
            "name": "acpp_omp_library_only",
            "features": ["sycl"],
            "cc": "gcc",
            "cxx": "g++",
            "features": [],
            "extras": {
                "cmake_configuration": [
                    "-DNESO_PARTICLES_SINGLE_COMPILED_LOOP=ON",
                    "-DACPP_TARGETS=omp.library-only",
                    "-DCMAKE_BUILD_TYPE=Release",
                ],
                "NUM_BUILD_WORKERS": 16,
                "NUM_MPI_RANKS": 8,
                "env_vars": {
                    "OMP_NUM_THREADS": 2,
                    "NESO_PARTICLES_DEVICE_AWARE_MPI": "ON",
                },
            },
            "modules": [
                "reframe/NP-acpp-llvm-cuda",
            ],
        },
    ],
}
