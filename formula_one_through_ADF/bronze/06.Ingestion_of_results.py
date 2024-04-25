# Databricks notebook source
# MAGIC %run ../formula_one_through_ADF/cmn_fun

# COMMAND ----------

from pyspark.sql.functions import col,explode,concat


# COMMAND ----------

result_df = spark.read.option('multiline',True).json('/mnt/sagen2databricks/f1-project/bronze/results/',recursiveFileLookup=True)
result_df.display()


# COMMAND ----------

result_df = result_df.withColumn('list',explode(col('MRData').RaceTable.Races))\
                .withColumn('lst',explode(col('list').Results))
result_df.display()


# COMMAND ----------

result_df =result_df.withColumn('driver_id',col('lst').Driver.driverid)\
            .withColumn('constructor_id',col('lst').Constructor.constructorId)\
            .withColumn('number',col('lst').number)\
            .withColumn('grid',col('lst').grid)\
            .withColumn('position',col('lst').position)\
            .withColumn('position_text',col('lst').positionText)\
            .withColumn('points',col('lst').points)\
            .withColumn('laps',col('lst').laps)\
            .withColumn('time',col('lst').time.time)\
            .withColumn('miliseconds',col('lst').time.millis)\
            .withColumn('fastestlap',col('lst').FastestLap.lap)\
            .withColumn('rank',col('lst').FastestLap.rank)\
            .withColumn('fastestlap_time',col('lst').FastestLap.Time.time)\
            .withColumn('fastestlap_speed',col('lst').FastestLap.AverageSpeed.speed)\
            .withColumn('status',col('lst').status)



result_df =result_df.drop('list','lst')
result_df.display()

# COMMAND ----------

result_df =result_df.withColumn('season',col('MRData').RaceTable.season)\
                    .withColumn('round',col('MRData').RaceTable.round)\
                    .withColumn('race_id',concat('season','round'))

result_df = result_df.drop('season','round','MRData')
result_df =result_df.select('race_id','driver_id','constructor_id','number','grid','position','position_text','points','laps','time','miliseconds','fastestlap','rank','fastestlap_time','fastestlap_speed','status')
result_df.display()
print(result_df.count())

# COMMAND ----------

result_df.columns


# COMMAND ----------

race_result = result_df.select('race_id','driver_id','constructor_id','number','grid','position','position_text','points','laps','time','miliseconds','fastestlap','rank','fastestlap_time','fastestlap_speed','status').distinct()
race_result.count()

# COMMAND ----------

race_result.write.option('format','delta').mode('overwrite').save('/mnt/sagen2databricks/f1-project/silver/results')

# COMMAND ----------

status_df = spark.read.load('/mnt/sagen2databricks/f1-project/silver/status')
result_df = result_df.join(status_df,'status')
result_df.display()