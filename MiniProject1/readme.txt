
Part 1a: Setting up Hadoop in Docker: 

Used to run the WordCount example program:
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar wordcount input/ output/

Used to concatenate and display the contents of all files in the "output" directory in HDFS:
hdfs dfs -cat output/*

-------------------------------------------------------------------------------------------------------------

Part 2: Developing a Hadoop program (N-Gram):

To transfer required file to HDFS directory /part2:
hdfs dfs -put ngram_input.txt /part2
hdfs dfs -put ngram_mapper.py /part2
hdfs dfs -put ngram_reducer.py /part2

Ran a Hadoop streaming job using custom Python scripts to process n-gram frequencies in the input file:
bin/hadoop jar share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
-files ngram_mapper.py,ngram_reducer.py \
-mapper "python3 ngram_mapper.py" \
-reducer "python3 ngram_reducer.py" \
-input /ngram_input.txt \
-output /output_ngram

hdfs dfs -cat /output_ngram/*

-----------------------------------------------------------------------------------------------------------------

Part 3: Developing a Hadoop program to analyze real logs

To transfer required file to HDFS directory /part3:
hdfs dfs -put access_log /part3
hdfs dfs -put part3_mapper.py /part3
hdfs dfs -put part3_reducer.py /part3

bin/hadoop jar share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
-file part3_mapper.py,part3_reducer.py \
-mapper "python3 part3_mapper.py" \
-reducer "python3 part3_reducer.py" \
-input /access_log \
-output /output_part3final

hdfs dfs -cat /output_part3final/*

bin/hadoop jar share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
-file part3_q4910_mapper.py,part3_q4910_reducer.py \
-mapper "python3 part3_q4910_mapper.py" \
-reducer "python3 part3_q4910_reducer.py" \
-input /access_log \
-output /output_part3q4910

hdfs dfs -cat /output_part3q4910/*

-------------------------------------------------------------------------------------------------------------------