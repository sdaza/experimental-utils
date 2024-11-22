# Experiment utils

Generic functions for experiment analysis and design

- [Experimental utils](#experimental-utils)
- [Installation](#installation)
- [How to use it](#how-to-use-it)
    - [Experiment Analyzer](#experiment-analyzer)
	- [Power Analysis](#power-analysis)

# Installation 

```
pip install git+https://github.com/sdaza/experiment-utils.git
```

# How to use it

## Experiment Analyzer


```python
analyzer = ExperimentAnalyzer(
    df,
    treatment_col="treatment",
    group_col="group",
    outcomes=['registrations', 'visits'],
    covariates=covariates,
    instrument_col="instrument",
    experimental_units=["campaign_key"],
    adjustment=None)

analyzer.get_uplifts()
analyzer.results
```

## Power Analysis


```python
from experiment_utils import PowerSim
p = PowerSim(metric='proportion', relative_effect=False,
	variants=1, nsim=1000, alpha=0.05, alternative='two-tailed')

p.get_power(baseline=[0.33], effect=[0.03], sample_size=[3000])
```

