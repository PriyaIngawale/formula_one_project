# Databricks notebook source
# MAGIC %run ../formula_one_through_ADF/cmn_fun

# COMMAND ----------

constructor_df = spark.read.json('/mnt/sagen2databricks/f1-project/bronze/constructors/',recursiveFileLookup=True)
constructor_df.display()

# COMMAND ----------

from pyspark.sql.functions import col, explode

# COMMAND ----------

constructor_df = constructor_df.withColumn('list',explode(col('MRData').ConstructorTable.Constructors))
constructor_df = constructor_df.drop('MRData')
constructor_df.display()

# COMMAND ----------

constructor_df = constructor_df.withColumn('constructor_Id',col('list').constructorId).withColumn('name',col('list.name')).withColumn('nationality',col('list').nationality)
constructor_df =constructor_df.drop('list')
constructor_df.display()

# COMMAND ----------

constructor_df.columns

# COMMAND ----------

constructor_df = constructor_df.select('constructor_Id', 'name', 'nationality').distinct()
constructor_df.count()

# COMMAND ----------

constructor_df.write.option('format','delta').mode('overwrite').save('/mnt/sagen2databricks/f1-project/silver/constructors')