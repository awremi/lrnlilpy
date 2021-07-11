
SPARK_APP_NAME='sparkjob_template'

from contextlib import contextmanager
from pyspark import SparkContext, SparkConf

@contextmanager
def use_spark_context(appName):
    conf = SparkConf().setAppName(appName) 
    spark_context = SparkContext(conf=conf)

    try:
        print("starting ", appName)
        yield spark_context
    finally:
        spark_context.stop()
        print("stopping ", appName)


with use_spark_context(appName=SPARK_APP_NAME) as sc:
    #----------------------
    # TODO: replace with your Spark code
    rdd = sc.range(100)
    #----------------------
