# Databricks notebook source
# MAGIC %run ../formula_one_through_ADF/cmn_fun

# COMMAND ----------

from pyspark.sql.functions import col,explode

# COMMAND ----------

circuit_df = spark.read.json('/mnt/sagen2databricks/f1-project/bronze/circuits/',recursiveFileLookup=True)
circuit_df.display()

# COMMAND ----------

circuit_df = circuit_df.withColumn('list',explode(col('MRData').CircuitTable.Circuits))
circuit_df = circuit_df.drop('MRData')
circuit_df.display()

# COMMAND ----------

circuit_df = circuit_df.withColumn('country',col('list').Location.country)\
    .withColumn('lat',col('list').Location.lat)\
    .withColumn('long',col('list').Location.long)\
    .withColumn('circuit_id',col('list').circuitid)\
    .withColumn('circuit_name',col('list').circuitName)
circuit_df = circuit_df.drop('list')
circuit_df.display()

# COMMAND ----------

circuit_df.columns

# COMMAND ----------

circuit_df = circuit_df.select('country', 'lat', 'long', 'circuit_id', 'circuit_name').distinct()
circuit_df.count()

# COMMAND ----------

circuit_df.write.option('format','delta').mode('overwrite').save('/mnt/sagen2databricks/f1-project/silver/circuits')