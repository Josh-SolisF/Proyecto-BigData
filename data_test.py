from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from functools import reduce

# Inicializar Spark
spark = SparkSession.builder \
    .appName("CargaPostgreSQL") \
    .config("spark.jars", "postgresql-42.5.0.jar") \
    .config("spark.executor.memory", "28g") \
    .config("spark.driver.memory", "28g") \
    .getOrCreate()

# --- FUNCIONES DE PREPROCESAMIENTO ---

def unificar_años(df):
    años_individuales = ["2006", "2007", "2008", "2009", "2010"]
    return df.withColumn(
        "reportyear",
        when(col("reportyear").isin(años_individuales), "2006-2010")
        .otherwise(col("reportyear"))
    )

def limpiar_desempleo(df):
    columnas = [c for c in df.columns if c not in ["_id", "reportyear"]]
    condiciones = [when((col(c).isNull()) | (col(c) == "Desconocido"), 1).otherwise(0) for c in columnas]
    condicion_nulos = reduce(lambda a, b: a + b, condiciones)
    return df.withColumn("nulos_count", condicion_nulos) \
             .filter(col("nulos_count") < 4) \
             .drop("nulos_count")

def limpiar_comida(df):
    columnas = [c for c in df.columns if c not in ["_id", "reportyear"]]
    condiciones = [when((col(c).isNull()) | (col(c) == "Desconocido"), 1).otherwise(0) for c in columnas]
    condicion_nulos = reduce(lambda a, b: a + b, condiciones)
    return df.withColumn("nulos_count", condicion_nulos) \
             .filter(col("nulos_count") < 4) \
             .drop("nulos_count")

# --- FUNCIONES DE CONEXIÓN CON POSTGRESQL ---

def leer_comida_postgres():
    print("Lectura de comida desde PostgreSQL")
    return spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://host.docker.internal:5433/postgres") \
        .option("user", "postgres") \
        .option("password", "pword") \
        .option("dbtable", "datos_comida") \
        .load()

def leer_desempleo_postgres():
    print("Lectura de desempleo desde PostgreSQL")
    return spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://host.docker.internal:5433/postgres") \
        .option("user", "postgres") \
        .option("password", "pword") \
        .option("dbtable", "datos_desempleo") \
        .load()

def guardar_union_postgres(df):
    df.repartition(10).write \
        .format("jdbc") \
        .option("batchsize", 1000) \
        .option("url", "jdbc:postgresql://host.docker.internal:5433/postgres") \
        .option("user", "postgres") \
        .option("password", "pword") \
        .option("dbtable", "datos_comida_desempleo") \
        .mode("overwrite") \
        .save()
    print("Datos combinados guardados en PostgreSQL")


# --- FLUJO PRINCIPAL ---

comida_df = leer_comida_postgres()
desempleo_df = leer_desempleo_postgres()

# Preprocesamiento
desempleo_df = unificar_años(desempleo_df)
desempleo_limpio = limpiar_desempleo(desempleo_df)
df_comida_limpio = limpiar_comida(comida_df)

# Renombrar columnas antes del join
df_comida_limpio = prefix_columns(df_comida_limpio, "comida")
desempleo_df_renamed = prefix_columns(desempleo_limpio, "desemp")

# Realizar unión
df_union = desempleo_df_renamed.join(df_comida_limpio, on="geotypevalue", how="inner")

# Guardar en PostgreSQL
guardar_union_postgres(df_union)
