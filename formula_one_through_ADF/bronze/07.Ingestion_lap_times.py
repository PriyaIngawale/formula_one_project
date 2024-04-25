# Databricks notebook source
# MAGIC %run ../formula_one_through_ADF/cmn_fun

# COMMAND ----------

lap_df = spark.read.json('/mnt/sagen2databricks/f1-project/bronze/lap_times/',recursiveFileLookup=True,multiLine=True)
lap_df.display()

# COMMAND ----------

from pyspark.sql.functions import col,explode,concat

# COMMAND ----------

lap_df = lap_df.withColumn('list',explode(col('MRData').RaceTable.Races))\
                .withColumn('lst',explode(col('list').Laps))\
                .withColumn('ls',explode(col('lst').Timings))


# COMMAND ----------

lap_df1 =lap_df.withColumn('driver_id',col('ls').driverid)\
            .withColumn('lap',col('lst').number)\
            .withColumn('position',col('ls').position)\
            .withColumn('time',col('ls').time)
lap_df1 =lap_df1.withColumn('season',col('MRData').RaceTable.season)\
                    .withColumn('round',col('MRData').RaceTable.round)\
                    .withColumn('race_id',concat('season','round'))

lap_df1 = lap_df1.drop('season','round','MRData','list','lst','ls')
lap_df1 =lap_df1.select('race_id','driver_id','lap','position','time')
lap_df1.display()
print(lap_df1.count())

# COMMAND ----------

lap_times_df = lap_df1.select('race_id','driver_id', 'lap', 'position', 'time').distinct()
lap_times_df.count()

# COMMAND ----------

lap_times_df.write.option('format','delta').mode('overwrite').save('/mnt/sagen2databricks/f1-project/silver/lap_times')