
from contextlib import contextmanager
from pyspark import SparkContext, SparkConf
import random

SPARK_APP_NAME='pi'

def random_point(x):
    return (random.random(), random.random())

def inside(p):
    x, y = p
    return x*x + y*y < 1

def pi_approximation(spark_context, num_samples):
    """ Approximate pi via Monte Carlo method"""
    count = spark_context.range(num_samples).map(random_point).filter(inside).count()
    pi = 4 * count / num_samples
    return pi

@contextmanager
def use_spark_context(sparkAppName):
    conf = SparkConf().setAppName(sparkAppName) 
    spark_context = SparkContext(conf=conf)

    try:
        yield spark_context
    finally:
        spark_context.stop()

with use_spark_context(SPARK_APP_NAME) as spark_context:
    num_samples = 100000000
    pi = pi_approximation(spark_context, num_samples)
    print()
    print("RESULT: pi is approximately ", pi)
    print()
