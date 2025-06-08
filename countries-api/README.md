## Countries API Documentation

A FastAPI application backed by MongoDB that provides rich, queryable information about all the world’s countries.

---

## 🚀 Features

* **Core Endpoints**
  – List **all** countries with filtering, sorting & pagination
  – Retrieve by **numeric ID**, **alpha-2**, **alpha-3** or **CIOC** code
* **Search & Filter**
  – Fuzzy/full-text search by name or capital
  – Filter by region, subregion, landlocked status
  – Filter by language, currency, demonym or translation
* **Statistical Queries**
  – Filter by area or population range
  – Sort by population density
* **Special Features**
  – Random country sampling
  – Compare multiple countries side-by-side
* **Metadata**
  – List all distinct regions, subregions, languages & currencies
* **Flexible Responses**
  – `fields` projection parameter to select only the properties you need
* **Robust Validation & Docs**
  – Pydantic models and FastAPI’s built-in validation
  – Interactive Swagger UI at `/docs`

---

## 📦 Technology Stack

* **Python 3.10+**
* **FastAPI** for web framework
* **Uvicorn** as ASGI server
* **MongoDB** for document storage
* **Motor** (asyncio) driver for MongoDB
* **Pydantic** for data validation

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/countries-api.git
   cd countries-api
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Unix/macOS
   .venv\Scripts\activate         # Windows PowerShell/CMD
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:

   ```
   MONGO_URI=mongodb://localhost:27017
   ```

   (add your credentials or cloud-URI if necessary)

5. **Import country data**
   Use the provided import script to fetch & load all countries in the desired schema:

   ```bash
   python scripts/import_countries.py
   ```

6. **(Optional) Enrich with interesting facts**

   ```bash
   python scripts/enrich_countries.py
   ```

---

## 📁 Project Structure

```
countries-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI instantiation & router inclusion
│   ├── config.py            # Settings & environment loading
│   ├── database.py          # MongoDB connection (Motor client)
│   ├── crud.py              # Async DB operations
│   ├── routes/
│   │   ├── __init__.py
│   │   └── countries.py     # All API endpoints
│   └── utils/
│       ├── __init__.py
│       └── enrichment.py    # Optional data enrichment scripts
│
├── scripts/
│   ├── import_countries.py  # Fetch & transform REST Countries data
│   └── enrich_countries.py  # Generate & store interesting facts via Gemini
│
├── tests/                   # pytest suite (fixtures & tests)
│
├── .env                     # Environment variables
├── requirements.txt
├── README.md                # (You are here!)
├── Dockerfile               # Containerization instructions
└── docker-compose.yml       # Local dev stack (MongoDB + app)
```

---

## 🔗 Configuration

* **`MONGO_URI`**
  MongoDB connection string (including credentials if required).
* **Port & Host**
  By default, Uvicorn serves on `127.0.0.1:8000`. Override via CLI flags or env vars.

---

## 📖 API Endpoints

All routes are prefixed with `/v1` and return JSON.

### Core Country Endpoints

| Route              | Method | Description                                                |
| ------------------ | :----: | ---------------------------------------------------------- |
| `/v1/all`          |   GET  | List all countries with optional `fields`, `sort`, filters |
| `/v1/id/{id}`      |   GET  | Get country by numeric `_id`                               |
| `/v1/alpha/{code}` |   GET  | Get by ISO-2, ISO-3 or CIOC code                           |

### Search & Filter

| Route                    | Method | Query Params      | Description       |
| ------------------------ | :----: | ----------------- | ----------------- |
| `/v1/search`             |   GET  | `q`: country name | Fuzzy name search |
| `/v1/name/{countryName}` |   GET  | None              | Exact name        |
| `/v1/capital/{capital}`  |   GET  | None              | Filter by capital |

### Geographical

| Route                       | Method | Description                |
| --------------------------- | :----: | -------------------------- |
| `/v1/region/{region}`       |   GET  | Countries in a region      |
| `/v1/subregion/{subregion}` |   GET  | Countries in a subregion   |
| `/v1/bordering/{code}`      |   GET  | Countries sharing a border |
| `/v1/landlocked`            |   GET  | All landlocked countries   |

### Cultural & Linguistic

| Route                           | Method | Description                               |
| ------------------------------- | :----: | ----------------------------------------- |
| `/v1/currency/{currency}`       |   GET  | Countries using a currency                |
| `/v1/lang/{language}`           |   GET  | Countries by language code                |
| `/v1/translation/{translation}` |   GET  | Countries with a specific translation key |
| `/v1/demonym/{name}`            |   GET  | Countries by demonym                      |

### Statistical

| Route            | Method | Query Params           | Description                |                            |
| ---------------- | :----: | ---------------------- | -------------------------- | -------------------------- |
| `/v1/area`       |   GET  | `min`, `max`, `region` | Filter by area range       |                            |
| `/v1/density`    |   GET  | \`sort=asc             | desc\`                     | Sort by population density |
| `/v1/population` |   GET  | `min`, `max`, `region` | Filter by population range |                            |

### Special Features

| Route                  | Method | Query Params        | Description                |
| ---------------------- | :----: | ------------------- | -------------------------- |
| `/v1/countries/random` |   GET  | `count=1–100`       | Get random country(ies)    |
| `/v1/compare`          |   GET  | `codes=USA,IND,...` | Compare multiple countries |

### Metadata

| Route                 | Method | Description                      |
| --------------------- | :----: | -------------------------------- |
| `/v1/meta/regions`    |   GET  | List all distinct regions        |
| `/v1/meta/subregions` |   GET  | List all distinct subregions     |
| `/v1/meta/languages`  |   GET  | List all distinct language codes |
| `/v1/meta/currencies` |   GET  | List all distinct currency codes |

---

## 📌 Query Parameters (All Endpoints)

* **`fields`**: Comma-separated list of document fields to include
* **`sort`**: Field to sort by (`-` prefix for descending)
* **`unMember`**: `true`/`false` to filter by UN membership
* **`independent`**: `true`/`false` to filter by independence

Plus route-specific filters as documented above.

---

## 🛠 Error Handling

* **400–422**: Validation errors (invalid query or path parameters)
* **404**: Resource not found (`Country not found`)
* **502**: Upstream/database errors
* **500**: Internal server errors

Custom exception handlers ensure consistent JSON error responses:

```json
{
  "error": "Detailed message",
  "path": "/v1/all"
}
```

---

## 📖 Interactive Docs

Once running (`uvicorn app.main:app --reload`), visit:

* **Swagger UI**:
  `http://127.0.0.1:8000/docs`
* **ReDoc**:
  `http://127.0.0.1:8000/redoc`

---

## ✅ Contributing

1. Fork the repo & create a new branch
2. Write tests under `tests/`
3. Lint & format with `black`/`flake8`
4. Submit a pull request

---

## 🎉 License

This project is licensed under the MIT License.
