from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
with DAG(
    'themapark_etl',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email': ['qkqhdksi0@gmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 4,  # 재시도 횟수
        'retry_delay': timedelta(minutes=3),  # 재시도 딜레이 - 3분
    },
    description='Themapark ETL Project',
    schedule=timedelta(days=1), # 반복날짜 - 1일마다
    start_date=datetime(2022, 10, 29, 2, 20),  # 시작날짜
    catchup=False,
    tags=['themapark_etl'],
) as dag:

    # 태스크들 추가
    # ㅡㅡㅡㅡㅡㅡ EXTRACT ㅡㅡㅡㅡㅡㅡ
    t1 = BashOperator(
        task_id='extract_today_weather',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract today_weather',
    )

    t2 = BashOperator(
        task_id='extract_today_dust',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract today_dust',
    )

    t3 = BashOperator(
        task_id='extract_pre_weather',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract pre_weather',
    )

    t4 = BashOperator(
        task_id='extract_pre_dust',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract pre_dust',
    )

    t5 = BashOperator(
        task_id='extract_navi_search',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract navi_search',
    )
    
    t6 = BashOperator(
        task_id='extract_event_childpark',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract event_childpark',
    )

    t7 = BashOperator(
        task_id='extract_event_seoulpark',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract event_seoulpark',
    )
    
    t8 = BashOperator(
        task_id='extract_everland_info',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract everland_info',
    )

    t9 = BashOperator(
        task_id='extract_lotteworld_info',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract lotteworld_info',
    )

    t18 = BashOperator(
        task_id='extract_holiday',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract holiday',
    )

    t20 = BashOperator(
        task_id='extract_subway_inout',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py extract subway_inout',
    )

    # ㅡㅡㅡㅡㅡㅡ TRANSFORM ㅡㅡㅡㅡㅡㅡ
    t10 = BashOperator(
        task_id='transform_today_weather',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py transform today_weather',
    )

    t11 = BashOperator(
        task_id='transform_today_dust',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py transform today_dust',
    )

    t12 = BashOperator(
        task_id='transform_themepark_event',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py transform themepark_event',
    )

    t13 = BashOperator(
        task_id='transform_navi_search',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py transform navi_search',
    )

    t21 = BashOperator(
        task_id='transform_subway_inout',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py transform subway_inout',
    )

    # ㅡㅡㅡㅡㅡㅡ DATAMART ㅡㅡㅡㅡㅡㅡ
    t14 = BashOperator(
        task_id='datamart_pre_air_weather',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py transform pre_air_weather',
    )    

    t15 = BashOperator(
        task_id='datamart_pre_themepark_event',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py datamart pre_themepark_event',
    )

    t19 = BashOperator(
        task_id='datamart_holiday',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py datamart holiday',
    )

    # ㅡㅡㅡㅡㅡㅡ OPERATION ㅡㅡㅡㅡㅡㅡ    
    t16 = BashOperator(
        task_id='operation_themepark_time',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py operation themepark_time',
    )

    t17 = BashOperator(
        task_id='operation_themepark_hol_fac',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py operation themepark_hol_fac',
    )

    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
    )

    # 태스크 우선순위 설정
    # extract는 병렬로, transform과 datamart는 직렬로
    
    t1 >> t10
    t2 >> t11
    t3 >> t4 >> t14
    t5 >> t13
    t18 >> t19
    [t6, t7] >> t12 >> t15
    [t8, t9] >> t16 >> t17
    t20 >> t21
    
    # t9 >> t10

  

