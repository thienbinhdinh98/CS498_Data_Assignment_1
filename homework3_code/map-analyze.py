import findspark

findspark.init()

import pyspark
import sys
import json

if len(sys.argv) != 3:
    raise Exception("Need 2 argument")

inputUri = sys.argv[1]
outputUri = sys.argv[2]

def MapFunction(x):
    return (len(x), 1)


def ReduceFunction(v1,v2):
    return v1+v2


sc = pyspark.SparkContext()
print("Spark context initialized")

lines = sc.textFile(sys.argv[1])

sentence_count = lines.flatMap(lambda line: line.split("\n") )

#print(len(lines.collect()))
#words = lines.flatMap(lambda line: line.split())
#print(words.collect())

print("Begin map reduce")
sentence_count  =  sentence_count.map(MapFunction).reduceByKey(ReduceFunction)

count_dict = sentence_count.collectAsMap()


print("Done")
#print(sentence_count.collect())
#this could be changed
sentence_count.saveAsTextFile(sys.argv[2])
with open("sentence_count.json", "w") as outfile:
    json.dump(count_dict, outfile)

print("Saved")

