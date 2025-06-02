# Standorte der Polizeidienststellen in Schleswig-Holstein

[![Lint css files](https://github.com/oklabflensburg/open-emergency-map/actions/workflows/lint-css.yml/badge.svg)](https://github.com/oklabflensburg/open-emergency-map/actions/workflows/lint-css.yml)
[![Lint html files](https://github.com/oklabflensburg/open-emergency-map/actions/workflows/lint-html.yml/badge.svg)](https://github.com/oklabflensburg/open-emergency-map/actions/workflows/lint-html.yml)
[![Lint js files](https://github.com/oklabflensburg/open-emergency-map/actions/workflows/lint-js.yml/badge.svg)](https://github.com/oklabflensburg/open-emergency-map/actions/workflows/lint-js.yml)
[![Lighthouse CI](https://github.com/oklabflensburg/open-emergency-map/actions/workflows/lighthouse.yml/badge.svg)](https://github.com/oklabflensburg/open-emergency-map/actions/workflows/lighthouse.yml)


![Screenshot Karte der Polizeidienststellen in Schleswig-Holstein](https://raw.githubusercontent.com/oklabflensburg/open-emergency-map/main/screenshot_notfallkarte.webp)


Standorte und Kontaktdaten der Polizeidienststellen in Schleswig-Holstein



## Hintergrund

Das Projekt wurde von ehrenamtlichen Mitgliedern des OK Lab Flensburg im Rahmen des [Code for Germany](https://codefor.de) Netzwerks entwickelt. Die Idee entstand im Zuge der Corona-Pandemie, um die Suche nach Polizeidienststellen in Schleswig-Holstein zu erleichtern. Die Karte wurde mit dem Ziel entwickelt, eine einfache und schnelle Möglichkeit zu bieten, Polizeidienststellen in der Umgebung zu finden.


## Datenquelle

Unsere Karte basiert auf dem Datensatz Polizeidienststellen in Schleswig-Holstein aus dem [Open Data Portal](https://opendata.schleswig-holstein.de/collection/polizeidienststellen) Schleswig-Holstein und wird jährlich aktualisiert.


## Mitmachen

Du kannst jederzeit ein Issue auf GitHub öffnen oder uns über oklabflensburg@grain.one schreiben



## How to Build

You must execute this commands in the root directory. Make sure you have node installed on your machine, then install dependencies. 

```
pnpm install
```


When you want to build the project run the following command

```
pnpm build
```


When you are developing on your local machine run this command

```
pnpm start
```



## Prerequisite

Install system dependencies and clone repository

```
sudo apt install git git-lfs virtualenv python3 python3-pip postgresql-16 postgresql-16-postgis-3 postgis
git clone https://github.com/oklabflensburg/open-emergency-map.git
```

Create a dot `.env` file inside root directory. Make sure to add the following content repaced by your own values

```
PARCEL_BASE_API_URL=https://api.oklabflensburg.de
PARCEL_BASE_URL=http://localhost

PARCEL_CONTACT_MAIL=mail@example.com
PARCEL_CONTACT_PHONE="+49xx"

PARCEL_PRIVACY_CONTACT_PERSON="Firstname Lastname"

PARCEL_ADDRESS_NAME="Address Name"
PARCEL_ADDRESS_STREET="Address Street"
PARCEL_ADDRESS_HOUSE_NUMBER="House Number"
PARCEL_ADDRESS_POSTAL_CODE="Postal Code"
PARCEL_ADDRESS_CITY="City"

DB_PASS=oklab
DB_HOST=localhost
DB_USER=oklab
DB_NAME=oklab
DB_PORT=5432
```


## Update repository

```
git pull
git lfs pull
```


## Create SQL schema

Run sql statements inside `open-emergency-map` root directory to create schema.

```
psql -U oklab -h localhost -d oklab -p 5432 < data/sh_police_station_schema.sql
```


## Import inventory

Required when you want to fetch data via API or want to update dataset. When running the python scripts. Make sure you replace the arguments with your arguments.

```
cd tools
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python3 insert_police_stations.py --env ../.env --src ../data/polizeidienststellen.csv --verbose
deactivate
```


---


## How to Contribute

Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) guide for details on how to get involved.


---


## License

This repository is licensed under [CC0-1.0](LICENSE).