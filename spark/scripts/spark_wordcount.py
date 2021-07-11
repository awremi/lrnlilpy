
from contextlib import contextmanager
from pyspark import SparkContext, SparkConf
import argparse

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

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-t','--text', help='path to text data', required=True)
    args = vars(parser.parse_args())
    
    text_path = args["text"]

    with use_spark_context("WordCount") as spark:
        text_file = spark.textFile(text_path)
        counts = text_file  \
                     .flatMap(lambda line: line.split(".")) \
                     .flatMap(lambda sentence: sentence.split(" ")) \
                     .filter(lambda word: len(word) > 0) \
                     .map(lambda word: (word.lower(), 1)) \
                     .reduceByKey(lambda a, b: a + b) \
                     .sortBy(lambda pair: pair[1], ascending=False)
        for kv in counts.take(10):
            print(kv)
