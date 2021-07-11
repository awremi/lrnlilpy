
SPARK_APP_NAME='sparkjob_test'

import sys
from contextlib import contextmanager
from pyspark import SparkContext, SparkConf

@contextmanager
def use_spark_context(appName):
    conf = SparkConf().setAppName(appName) 
    spark_context = SparkContext(conf=conf)

    try:
        print("starting ", SPARK_APP_NAME)
        yield spark_context
    finally:
        spark_context.stop()
        print("stopping ", SPARK_APP_NAME)


with use_spark_context(appName=SPARK_APP_NAME) as sc:
    rdd = sc.range(100)
    print()
    print("##########################################")
    print("PySpark uses Python version: ", sys.version)
    print("Congratulations, submitting a PySpark job is working")
    print("##########################################")
    print()
