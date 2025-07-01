# Prototype NESO Reframe Testing Scripts

## Dependencies
* spack
* reframe

## How this works

If this repository is cloned at ``<root>`` then this tool assumes that a NESO to be tested exists at ``<root>/../NESO-reframe-stage``. This tool will use the spack environments it is bundled with to build NESO and run the tests.

Create a configuration file for your machine, e.g. ``config/baseline_P0818.py`` then run with:


```
reframe -C config/baseline_P0818.py -c build_run_tests.py -r 
```


