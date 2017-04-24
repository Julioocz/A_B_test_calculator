"""
    A/B split test calculator
    ----------
        
    This module implements the statistical calculation of the A/B test split significance. The 
    implementation was taken from https://www.periscopedata.com/blog/ab-testing-in-redshift.html
    which contains the code to do the statistical analysis using the normal approximation method 
    in redshift with scipy. This was translated to python using scipy too.
"""

from scipy.stats import norm


def standard_error(sample_size, successes):
    """
    Calculates the standard error of a sample proportion.
    
    Formula: σp = sqrt [ p(1 - p) / n ]. 
    with:
    p = proportion of successes in sample (successes / sample size)    
    
    :param sample_size: the size of the sample 
    :param successes: the number of successes on the given sample. 
    :return: the standard error on the sample proportion -> σp
    """
    p = successes / sample_size
    return (p * (1 - p) / sample_size) ** 0.5


def significance(size_a, successes_a, size_b, successes_b):
    """
    Calculates the significance for an A/B test.
    
    :param size_a: Sample size of the experiment A
    :param successes_a: Successes of the experiment A
    :param size_b: Sample size fo the experiment B
    :param successes_b: Successes of the experiment b
    :return: The significance of the test.
    """
    # Raising an error if the condition of size_sample > successes is not met.
    if size_a < successes_a or size_b < successes_b:
        raise ValueError('The size numbers must be greater than the number of successes for an '
                         'experiment')

    p_a = successes_a / size_a
    p_b = successes_b / size_b
    se_a = standard_error(size_a, successes_a)
    se_b = standard_error(size_b, successes_b)

    numerator = (p_b - p_a)
    denominator = (se_a ** 2 + se_b ** 2) ** 0.5

    return norm.sf(abs(numerator / denominator))
