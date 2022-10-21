from pyspark.sql.functions import ceil, col
from infra.spark_session import get_spark_session
from infra.jdbc import DataWarehouse, DataMart, find_data, save_data

class CoPopuDensity:

    @classmethod
    def save(cls):
        # DW에서 테이블 읽어오기
        popu = find_data(DataWarehouse, 'LOC')
        patients = find_data(DataWarehouse, 'CORONA_PATIENTS')
        pop_patients = cls.__generate_data(popu, patients)
        # DM에 저장
        save_data(DataMart, pop_patients, 'CO_POPU_DENSITY')

    @classmethod
    def __generate_data(cls, popu, patients):
        pop_patients = popu.join(patients, on='loc') \
                                .select('loc', ceil(col('population') / col('area')).alias('popu_density'), 'qur_rate', 'std_day') \
                                .orderBy(col('std_day'))
        return pop_patients