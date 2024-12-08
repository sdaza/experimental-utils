import pytest
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from experiment_utils.experiment_analyzer import ExperimentAnalyzer
from experiment_utils.spark_instance import *

import numpy as np
import pandas as pd
from scipy.stats import truncnorm


@pytest.fixture
def sample_data(
    n_model=1000,
    n_random=500,
    base_model_conversion_mean=0.3,
    base_model_conversion_variance=0.01,
    base_random_conversion_mean=0.10,
    base_random_conversion_variance=0.01,
    model_treatment_effect=0.05,
    random_treatment_effect=0.05,
    random_seed=42,
):

    np.random.seed(random_seed)

    # Function to get a truncated normal distribution
    def get_truncated_normal(mean, variance, size):
        std_dev = np.sqrt(variance)
        lower, upper = 0, 1
        a, b = (lower - mean) / std_dev, (upper - mean) / std_dev
        return truncnorm.rvs(a, b, loc=mean, scale=std_dev, size=size)

    # Generate baseline conversions with a truncated normal distribution
    base_model_conversion = get_truncated_normal(
        base_model_conversion_mean, base_model_conversion_variance, n_model
    )
    base_random_conversion = get_truncated_normal(
        base_random_conversion_mean, base_random_conversion_variance, n_random
    )

    # model group data
    model_treatment = np.random.binomial(1, 0.8, n_model)
    model_conversion = (
        base_model_conversion + model_treatment_effect * model_treatment
    ) > np.random.rand(n_model)
    
    model_data = pd.DataFrame(
        {
            "experiment": 123,
            "group": "model",
            "treatment": model_treatment,
            "conversion": model_conversion.astype(int),
            "baseline_conversion": base_model_conversion,
        }
    )

    # random group data
    random_treatment = np.random.binomial(1, 0.5, n_random)
    random_conversion = (
        base_random_conversion + random_treatment_effect * random_treatment
    ) > np.random.rand(n_random)
    random_data = pd.DataFrame(
        {
            "experiment": 123,
            "group": "random",
            "treatment": random_treatment,
            "conversion": random_conversion.astype(int),
            "baseline_conversion": base_random_conversion,
        }
    )

    # Combine data
    data = pd.concat([model_data, random_data])
    df = spark.createDataFrame(data)

    return df


def test_no_covariates(sample_data):
    """Test get_effects no covariates"""
    outcomes = "conversion"
    treatment_col = "treatment"
    experiment_identifier = "experiment"

    analyzer = ExperimentAnalyzer(
        data=sample_data,
        outcomes=outcomes,
        treatment_col=treatment_col,
        experiment_identifier=experiment_identifier)
    

    # This should not raise an error since all columns are present
    try:
        analyzer.get_effects()
        analyzer.results
        assert True
    except Exception as e:
        pytest.fail(f" raised an exception: {e}")


def test_no_adjustment(sample_data):
    """Test get_effects no adjustments"""
    outcomes = "conversion"
    treatment_col = "treatment"
    experiment_identifier = "experiment"
    covariates = "baseline_conversion"

    analyzer = ExperimentAnalyzer(
        data=sample_data,
        outcomes=outcomes,
        treatment_col=treatment_col,
        experiment_identifier=experiment_identifier,
        covariates=covariates
    )

    # This should not raise an error since all columns are present
    try:
        analyzer.get_effects()
        analyzer.results
        assert True
    except Exception as e:
        pytest.fail(f" raised an exception: {e}")