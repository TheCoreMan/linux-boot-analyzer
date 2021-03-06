"""
Code loosely based on http://www.postgresqltutorial.com/postgresql-python/connect/
"""
import pprint
from configparser import ConfigParser

import psycopg2
from flask import Flask, request


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config(filename='database.ini', section='postgresql')
        """
        THIS FILE WILL NOT BE ON SOURCE CONTROL. 
        Create a "secret.ini" file like this: 
        
            [postgresql]
            password=PUT_DATABASE_PASSWORD_HERE
        
        """
        secret = config(filename='secret.ini', section='postgresql')
        params["password"] = secret["password"]

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        print("Config parameters:" + str(params))
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


app = Flask(__name__)


@app.route("/report_analysis", methods=['POST'])
def report_analysis():
    report_data = request.json
    pprint.pprint(report_data)
    return "Awesome, dude."


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
