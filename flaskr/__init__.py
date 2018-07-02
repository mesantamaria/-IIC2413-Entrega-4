#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
# import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "data"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]


#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = 'queries'
QUERIES_FILENAME = '/var/www/Entrega4/queries'



@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)


@app.route("/mongo")
def mongo():
    query = request.args.get("query")
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    if "find" in query:
        return render_template('mongo.html', results=results)
    else:
        return "ok"


@app.route("/users/<uname>", methods=['GET'])
def find_user(uname):
    output = []
    for doc in mongodb.mensajes.find({"nombre": uname}):
        output.append(doc['alias'])
    return jsonify(output)


@app.route("/ultimo_alias/<uname>", methods=['GET'])
def find_last_alias(uname):
    output = []
    #doc = mongodb.mensajes.find({"nombre": uname}).sort({"fecha": 1})
    for doc in mongodb.mensajes.find({"nombre": uname}).sort({"fecha": 1}):
        output.append({'alias': doc['alias'], 'fecha': doc['fecha']})
    return jsonify(output)


@app.route("/example")
def example():
    return render_template('example.html')


if __name__ == "__main__":
    app.run()
