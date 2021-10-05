try:
    import requests
    import os
    from datetime import date
    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime
    import pandas as pd

    print("All Dag modules are ok ......")
except Exception as e:
    print("Error  {} ".format(e))


def first_function_execute(stock_ticker, **context):
    print("first_function_execute   ")
    context['ti'].xcom_push(key='mykey', value="first_function_execute says Hello ")
    my_portfolio = ("MSFT", "BRKB", "TAN", "FSLR", "VOO")
    today = date.today()
    todays_date = today.strftime("%b-%d-%Y")
    stocks_list = []
    API_KEY = 'f74ba0d0d10414840495409424bdc224'  # need to pass key manually for now don't know how to pass api key in continaer
    stock_list = stock_ticker
    params = {
        'access_key': API_KEY,
        'symbols': stock_list}
    api_result = requests.get('http://api.marketstack.com/v1/intraday/latest', params)
    api_response = api_result.json()
    for stock_data in api_response['data']:
        stocks_list.append([todays_date, stock_data['symbol'], stock_data['last']])   #only returning las telement will fix later
    print(stocks_list)

def second_function_execute(**context):
    shares_owned = [1, 2, 3, 4, 5]
    instance = context.get("ti").xcom_pull(key="mykey")
    data = [{"name":"Soumil","title":"Full Stack Software Engineer"}, { "name":"Nitin","title":"Full Stack Software Engineer"},]
    dates = [sublist[0] for sublist in STOCKS_LIST]
    stock_codes = [sublist[1] for sublist in STOCKS_LIST]
    price = [STOCKS_LIST[0][2] * shares_owned[i] for i in range(len(shares_owned))]
    final_list = []

with DAG(
        dag_id="first_dag",
        schedule_interval="@daily",
        default_args={
            "owner": "airflow",
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
            "start_date": datetime(2021, 1, 1),
        },
        catchup=False) as f:

    first_function_execute = PythonOperator(
        task_id="first_function_execute",
        python_callable=first_function_execute,
        provide_context=True,
       # op_kwargs={"stock_ticker":"MSFT"} #provide args here
        op_kwargs = {"stock_ticker": ("MSFT", "BRKB", "TAN", "FSLR", "VOO")}
    )

    second_function_execute = PythonOperator(
        task_id="second_function_execute",
        python_callable=second_function_execute,
        provide_context=True,
    )

first_function_execute >> second_function_execute
