import io

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import collections
import pymongo
from django.conf import settings
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pandas as pd
import json
from bson import json_util
import urllib, base64
from django import forms


connect_string = "mongodb://db-django:RCW66AYz3nLpEzi0Xg38j6Rhyu82Q6lHtJdmy04zLZExvBAiW3riy9xXnu3b8PgsF6r09kAaodenBd55TKTR1g==@db-django.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@db-django@"


def Courses(request):
    ddl_code = 'TSLA'
    if request.method == "POST":
        ddl_code = request.POST["stock_var"]
        print(ddl_code)

    my_client = pymongo.MongoClient(connect_string)

    # First define the database name
    dbname = my_client['db-django']

    # Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
    collection_name = dbname["nasdaq_data"]

    # let's create two documents
    data1 = {
        "code": "MSFT",
        "datetime": "2022-03-25",
        "open": "305.23",
        "close": "303.68",
        "volume": "22566400"
    }
    data2 = {
        "code": "MSFT",
        "datetime": "2022-03-29",
        "open": "313.91",
        "close": "310.96",
        "volume": "6105132"
    }
    data3 = {
        "code": "MSFT",
        "datetime": "2022-04-01",
        "open": "309.37",
        "close": "306.56",
        "volume": "3795628"
    }
    data4 = {
        "code": "MSFT",
        "datetime": "2022-04-04",
        "open": "310.09",
        "close": "313.88",
        "volume": "4171486"
    }

    # Insert the documents
    # collection_name.insert_many([data1, data2, data3, data4])

    # Read the documents
    nasdaq_all_stock_code = collection_name.find()
    df_stocks = pd.DataFrame(list(nasdaq_all_stock_code))

    nasdaq_data = collection_name.find({'code': ddl_code})
    df = pd.DataFrame(list(nasdaq_data))

    print(df)

    df["datetime"] = pd.to_datetime(df.datetime, format="%Y-%m-%d")
    df.index = df['datetime']

    # plt.figure(figsize=(16, 8))

    fig, ax = plt.subplots()

    ax.plot(df['datetime'], df["close"])

    ax.set(xlabel='Date', ylabel='Close',
           title=ddl_code + ' - Nasdaq Stock Historical')

    ax.grid()

    # response = HttpResponse(content_type='image/png')
    # canvas = FigureCanvasAgg(fig)
    # canvas.print_png(response)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    uri = urllib.parse.quote(string)

    stock_codes = df_stocks['code'].unique()

    context = {'data': uri, 'stock_codes': stock_codes, 'ddl_code': ddl_code}

    return render(request, 'stock_historical.html', context)
    # return response


def detail(request, course_id):
    return HttpResponse('<h2>These are the course details for course id: ' + str(course_id) + '</h2>')


