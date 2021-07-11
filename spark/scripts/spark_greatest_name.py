
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
    parser.add_argument('-n','--names', help='path to names file, one name per line', required=True)
    args = vars(parser.parse_args())
    
    text_path = args["text"]
    names_path = args["names"]
    with open(names_path, "r") as names_file:
        names = [line.strip() for line in names_file]
        name_bigrams = [tuple(name.split(" ")) for name in names]

    print("input names: ", name_bigrams)
    with use_spark_context("The Greatest Name") as spark:
        text_file = spark.textFile(text_path)
        bigrams = text_file.flatMap(lambda line: line.split(".")) \
                           .map(lambda line: line.strip().split(" ")) \
                           .flatMap(lambda xs: (tuple(x) for x in zip(xs, xs[1:])))
        counts = bigrams.map(lambda bigram: (bigram, 1)) \
                .reduceByKey(lambda x, y: x + y) \
                .filter(lambda kv: kv[0] in name_bigrams) \
                .collect()
        print("Number of mentions for each name:")
        print(counts)
