import os
import sys
import csv
import click
import traceback
import logging as log
import psycopg2

from shapely.geometry import Point
from dotenv import load_dotenv
from pathlib import Path


# log uncaught exceptions
def log_exceptions(type, value, tb):
    exception_details = traceback.TracebackException(type, value, tb)

    for line in exception_details.format(chain=True):
        log.exception(line)

    log.exception(value)

    sys.__excepthook__(type, value, tb)  # calls default excepthook


def connect_database(env_path):
    try:
        load_dotenv(dotenv_path=Path(env_path))

        conn = psycopg2.connect(
            database=os.getenv('DB_NAME'),
            password=os.getenv('DB_PASS'),
            user=os.getenv('DB_USER'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )

        conn.autocommit = True

        log.info('connection to database established')

        return conn
    except Exception as e:
        log.error(e)

        sys.exit(1)


def parse_value(value, conversion_func=None):
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()
        if value == '':
            return None

    try:
        return conversion_func(value) if conversion_func else value
    except (ValueError, TypeError):
        return None


def insert_row(cur, row_dict):
    id = parse_value(row_dict.get('id'), int)
    name = parse_value(row_dict.get('name', ''))
    city = parse_value(row_dict.get('city', ''))
    zipcode = parse_value(row_dict.get('zipcode', ''))
    street = parse_value(row_dict.get('street', ''))
    house_number = parse_value(row_dict.get('house_number', ''))
    telephone = parse_value(row_dict.get('telephone', ''))
    fax = parse_value(row_dict.get('fax', ''))
    email = parse_value(row_dict.get('email', ''))
    website = parse_value(row_dict.get('website', ''))
    longitude = parse_value(row_dict.get('longitude'), float)
    latitude = parse_value(row_dict.get('latitude'), float)

    wkb_geometry = None

    if latitude is not None and longitude is not None:
        point = Point(longitude, latitude)
        wkb_geometry = point.wkb

    sql = '''
        INSERT INTO sh_police_station (id, name, city,
            zipcode, street, house_number, telephone, fax, email,
            website, longitude, latitude, wkb_geometry)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id)
        DO UPDATE SET
            name = EXCLUDED.name,
            city = EXCLUDED.city,
            zipcode = EXCLUDED.zipcode,
            street = EXCLUDED.street,
            house_number = EXCLUDED.house_number,
            telephone = EXCLUDED.telephone,
            fax = EXCLUDED.fax,
            email = EXCLUDED.email,
            website = EXCLUDED.website,
            longitude = EXCLUDED.longitude,
            latitude = EXCLUDED.latitude,
            wkb_geometry = EXCLUDED.wkb_geometry
        RETURNING id, (xmax = 0) AS inserted
    '''

    try:
        cur.execute(sql, (
            id, name, city, zipcode, street, house_number, telephone,
            fax, email, website, longitude, latitude, wkb_geometry
        ))

        result = cur.fetchone()
        last_id = result[0]
        is_insert = result[1]

        if is_insert:
            log.info(f'Inserted station {name} with id {last_id}')
        else:
            log.info(f'Updated station {name} with id {last_id}')

    except Exception as e:
        log.error(f'Error with station {name}: {e}')


def read_csv(conn, src):
    cur = conn.cursor()

    with open(src, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter='\t')

        for row in csv_reader:
            insert_row(cur, row)


@click.command()
@click.option(
    '--env', '-e', type=str, required=True, help='Path to local dot env file',
)
@click.option(
    '--src', '-s', type=str, required=True, help='Path to your local file'
)
@click.option(
    '--verbose', '-v', is_flag=True, help='Print more verbose output'
)
@click.option(
    '--debug', '-d', is_flag=True, help='Print detailed debug output'
)
def main(env, src, verbose, debug):
    if debug:
        log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)
    if verbose:
        log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)
        log.info('set logging level to verbose')
    else:
        log.basicConfig(format='%(levelname)s: %(message)s')

    recursion_limit = sys.getrecursionlimit()
    log.info(f'your system recursion limit: {recursion_limit}')

    conn = connect_database(env)
    read_csv(conn, src)


if __name__ == '__main__':
    sys.excepthook = log_exceptions

    main()
