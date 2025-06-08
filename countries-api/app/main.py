# countries-api/
# ├── app/                         # Main application package
# │   ├── __init__.py
# │   ├── main.py                  # FastAPI instantiation & router inclusion
# │   ├── config.py                # Settings (e.g. via pydantic’s BaseSettings  python-dotenv)
# │   ├── database.py              # MongoDB connection setup (Motor client)
# │   ├── models.py                # Pydantic schemas (Country, Currency, Language, etc.)
# │   ├── crud.py                  # Async functions for read/write against country_collection
# │   ├── routes/                  # All your API route modules
# │   │   ├── __init__.py
# │   │   └── countries.py         # `/countries` and `/countries/{alpha3}` endpoints
# │   └── utils/                   # Utility scripts/helpers
# │       ├── __init__.py
# │       └── enrichment.py        # e.g. merging “interestingFact” data
# │
# ├── scripts/                     # Stand-alone data tooling
# │   └── import_countries.py      # Script to fetch from REST Countries, transform & bulk-load into MongoDB
# │
# ├── tests/                       # Test suite
# │   ├── __init__.py
# │   ├── conftest.py              # pytest fixtures (e.g. test client, test DB setup/teardown)
# │   └── test_countries.py        # Unit/integration tests for your endpoints
# │
# ├── .env                         # Environment variables (MONGO_URI, API_KEYS, etc.)
# ├── requirements.txt             # Pinned dependencies
# ├── README.md                    # Project overview, setup & deploy instructions
# ├── Dockerfile                   # (Optional) Containerize your app
# └── docker-compose.yml           # (Optional) MongoDB  app stack for local dev


# # Core Country Endpoints
# /v1/all                             # Get all countries
# /v1/alpha/{code}                        # Search by cca2, ccn3, cca3 or cioc country code (yes, any!)
#
# # Search & Filter Endpoints
# /v1/search?q={countryName}          # Search by country name. If you want to get an exact match, use the next endpoint. It can be the common or official value
# /v1/name/{countryName}                  # Search by country name. If you want to get an exact match, use the next endpoint. It can be the common or official value
# /v1/capital/{capital}                   # Search by capital city name
#
# # Geographical Endpoints
# /v1/region/{region}                     # Search by region name (e.g. Africa, Americas, Asia, Europe, Oceania)
# /v1/subregion/{subregion}               # Search by subregion name (e.g. Northern America, Western Europe, South-Eastern Asia, etc.)
# /v1/bordering/{code}          # Search by cca2, ccn3, cca3 or cioc country code (yes, any!) and get all countries bordering it
# /v1/landlocked                # Get all landlocked countries
#
# # Cultural/Linguistic Endpoints
# /v1/currency/{currency}                 # Search by currency code or name (ISO 4217)
# /v1/lang/{language}                     # Search by language code or name (ISO 639-1 or ISO 639-2)
# /v1/translation/{translation}           # Search by translation code (ISO 639-1 or ISO 639-2) or name
# /v1/demonym/{name}                      # Search by demonym name (e.g. American, British, etc.)
#
# # Statistical Endpoints
# /v1/area?min={min}&max={max}&region={region}  # Get all countries with area in the specified range (in square kilometers) and in the specified region (if provided)
# /v1/density?sort={asc|desc}             # Get all countries sorted by population density (people per square kilometer)
# /v1/population?min={min}&max={max}&region={region}  # Get all countries with population in the specified range and in the specified region (if provided)
#
# # Special Feature Endpoints
# /v1/countries/random?count={count}  # Get a random country or countries (if count is specified, it must be between 1 and 100) from the database
# /v1/compare?codes={code},{code},{code}  # Search by cca2, ccn3, cca3 or cioc country codes (yes, any!)
#
# # Metadata Endpoints ebcrvlpRIOOyilLg
# /v1/meta/regions                   # Get all regions
# /v1/meta/subregions               # Get all subregions
# /v1/meta/languages               # Get all languages
# /v1/meta/currencies               # Get all currencies
#
# # Optional Query Parameters (All Endpoints)
# fields                          # Select specific fields | Comma-separated list of fields to include in the response (e.g. ?fields=name.common,population,areaKm2). Use the `fields` query parameter to specify which fields you want to include in the response. If not provided, all fields will be included.
# sort                           # Sort by field (asc/-desc) | Sort the results by a specific field (e.g. ?sort=-population). Use the `sort` query parameter to specify the field you want to sort by. If not provided, the results will not be sorted.
# unMember                      # Filter by UN member status | Filter the results by UN member status (e.g. ?unMember=true). Use the `unMember` query parameter to filter the results by UN member status. If not provided, all countries will be included.
# independent                   # Filter by independent status | Filter the results by independent status (e.g. ?independent=false). Use the `independent` query parameter to filterthe results by independent status. If not provided, all countries will be included.

from fastapi import FastAPI
from app.routes.countries import router as countries_router

app = FastAPI(
    title="Countries API",
    description="An API for country data",
    version="0.1.0",
)
app.include_router(countries_router)
