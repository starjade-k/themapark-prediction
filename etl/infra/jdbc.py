from enum import Enum
from infra.spark_session import get_spark_session

class DataWarehouse(Enum):
    URL ='jdbc:oracle:thin:@themapark_high?TNS_ADMIN=/home/big/pj/db/Wallet_themapark'
    PROPS={
        'user':'dw_themapark'
       ,'password':'123qwe!@#QWE'
    }

class DataMart(Enum):
    URL ='jdbc:oracle:thin:@themapark_high?TNS_ADMIN=/home/big/pj/db/Wallet_themapark'
    PROPS={
        'user':'dm_themapark'
       ,'password':'123qwe!@#QWE'
    }

class OpData(Enum):
    URL ='jdbc:oracle:thin:@themapark_high?TNS_ADMIN=/home/big/pj/db/Wallet_themapark'
    PROPS={
        'user':'op_themapark'
       ,'password':'123qwe!@#QWE'
    }

def save_data(config, dataframe, table_name):
    dataframe.write.jdbc(url=config.URL.value
                        , table=table_name
                        , mode='append'
                        , properties=config.PROPS.value)

def overwrite_data(config, dataframe, table_name):
    dataframe.write.jdbc(url=config.URL.value
                        , table=table_name
                        , mode='overwrite'
                        , properties=config.PROPS.value)

def overwrite_trunc_data(config, dataframe, table_name):
    dataframe.write.option("truncate", "true").jdbc(url=config.URL.value,
                                                    table=table_name,
                                                    mode='overwrite',
                                                    properties=config.PROPS.value)

def find_data(config, table_name):
    return get_spark_session().read.jdbc(url=config.URL.value
                                , table=table_name
                                , properties=config.PROPS.value)