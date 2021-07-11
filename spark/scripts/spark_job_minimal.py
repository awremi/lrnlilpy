
from pyspark import SparkContext, SparkConf

SPARK_APP_NAME='sparkjob_template'
conf = SparkConf().setAppName(SPARK_APP_NAME) 
spark_context = SparkContext(conf=conf)

#----------------------
# TODO: replace with your Spark code
rdd = spark_context.range(100)
#----------------------

spark_context.stop() # don't forget to cleanly shut down
