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
        'retries': 2,  # 재시도 횟수
        'retry_delay': timedelta(minutes=3),  # 재시도 딜레이 - 3분
    },
    description='Themapark ETL Project',
    schedule=timedelta(days=1), # 반복날짜 - 1일마다
    start_date=datetime(2022, 10, 26, 4, 20),  # 시작날짜
    catchup=False,
    tags=['themapark_etl'],
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    # 태스크들 추가
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
        task_id='transform_today_weather',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py transform today_weather',
    )

    t6 = BashOperator(
        task_id='transform_today_dust',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py transform today_dust',
    )

    # t7 = BashOperator(
    #     task_id='transform_pre_weather',
    #     cwd='/home/big/pj/ETL',
    #     bash_command='python3 main.py transform pre_weather',
    # )

    t8 = BashOperator(
        task_id='transform_pre_air_weather',
        cwd='/home/big/pj/ETL',
        bash_command='python3 main.py transform pre_air_weather',
    )    

    # t9 = BashOperator(
    #     task_id='datamart_today_weather',
    #     cwd='/home/big/pj/ETL',
    #     bash_command='python3 main.py datamart today_weather',
    # )

    # t10 = BashOperator(
    #     task_id='datamart_pre_air_weather',
    #     cwd='/home/big/pj/ETL',
    #     bash_command='python3 main.py datamart pre_air_weather',
    # )

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
    
    # t9 >> t10

  
