from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ASCENDING, DESCENDING
import random

# from app.database import country_collection  # type: AsyncIOMotorCollection
from app.database import country_collection, convert_mongo_doc  # type: AsyncIOMotorCollection


# Utility to build projection dict from comma-separated fields
def _build_projection(fields: Optional[str]) -> Optional[Dict[str, int]]:
    """
    Convert comma-separated field names into a MongoDB projection dictionary.

    Args:
        fields: Comma-separated string of field names to include in the result

    Returns:
        Dict mapping field names to 1 (include) or None if fields is None
    """
    if not fields:
        return None
    projection = {}
    for f in fields.split(","):
        projection[f.strip()] = 1
    return projection


async def get_all_countries(
    fields: Optional[str],
    sort: Optional[str],
    unMember: Optional[bool],
    independent: Optional[bool],
    limit: int,
    skip: int,
) -> List[Dict[str, Any]]:
    """
    Retrieve countries with optional filtering, sorting, and pagination.

    Args:
        fields: Comma-separated list of fields to include in the result
        sort: Field to sort by (prefix with "-" for descending order)
        unMember: Filter by UN membership status
        independent: Filter by independence status
        limit: Maximum number of countries to return
        skip: Number of countries to skip (for pagination)

    Returns:
        List of country documents matching the criteria
    """
    query: Dict[str, Any] = {}
    if unMember is not None:
        query["unMember"] = unMember
    if independent is not None:
        query["independent"] = independent

    projection = _build_projection(fields)
    cursor = country_collection.find(query, projection)
    # apply sort
    if sort:
        direction = ASCENDING if not sort.startswith("-") else DESCENDING
        field = sort.lstrip("-")
        cursor = cursor.sort(field, direction)
    # apply pagination
    cursor = cursor.skip(skip).limit(limit)
    # return cursor.to_list(length=limit)
    results = await cursor.to_list(length=limit)
    return [convert_mongo_doc(doc) for doc in results]


async def get_country_by_id(id: str, fields: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Find a country by its unique ID.

    Args:
        id: Unique identifier of the country document
        fields: Comma-separated list of fields to include in the result

    Returns:
        Country document if found, None otherwise
    """
    query = {"_id": id}
    projection = _build_projection(fields)
    # return await country_collection.find_one(query, projection)
    doc = await country_collection.find_one(query, projection)
    return convert_mongo_doc(doc) if doc else None


# Apply similar changes to all functions that return MongoDB documents
async def get_country_by_code(code: str, fields: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Find a country by its code (alpha2, alpha3, numeric, or CIOC).

    Args:
        code: Country code to search for
        fields: Comma-separated list of fields to include in the result

    Returns:
        Country document if found, None otherwise
    """
    # search multiple code fields
    query = {"$or": [
        {"alpha2Code": code.upper()},
        {"alpha3Code": code.upper()},
        {"numericCode": code},
        {"cioc": code.upper()},
    ]}
    projection = _build_projection(fields)
    # return await country_collection.find_one(query, projection)
    doc = await country_collection.find_one(query, projection)
    return convert_mongo_doc(doc) if doc else None


async def search_countries(
    q: str,
    fields: Optional[str],
    exact: bool = False,
) -> List[Dict[str, Any]]:
    """
    Search for countries by name (official or native).

    Args:
        q: Name or partial name to search for
        fields: Comma-separated list of fields to include in the result
        exact: Whether to perform exact match (True) or case-insensitive partial match (False)

    Returns:
        List of countries matching the search criteria
    """
    if exact:
        query = {"$or": [{"name": q}, {"nativeName": q}]}
    else:
        regex = {"$regex": q, "$options": "i"}
        query = {"$or": [{"name": regex}, {"nativeName": regex}]}
    projection = _build_projection(fields)
    cursor = country_collection.find(query, projection)
    results = await cursor.to_list(length=1000)
    return [convert_mongo_doc(doc) for doc in results]


# Simple filters by single field equality or regex
async def filter_by_capital(capital: str, fields: Optional[str]):
    """
    Find countries by capital city name (partial, case-insensitive match).

    Args:
        capital: Capital city name pattern to search for
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries matching the capital city pattern
    """
    query = {"capital": {"$regex": capital, "$options": "i"}}
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def filter_by_region(region: str, fields: Optional[str]):
    """
    Find countries in a specific region.

    Args:
        region: Region name to filter by
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries in the specified region
    """
    query = {"region": region}
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def filter_by_subregion(subregion: str, fields: Optional[str]):
    """
    Find countries in a specific subregion.

    Args:
        subregion: Subregion name to filter by
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries in the specified subregion
    """
    query = {"subregion": subregion}
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def filter_by_border(code: str, fields: Optional[str]):
    """
    Find countries that border a specific country.

    Args:
        code: Alpha-3 country code to find neighboring countries
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries bordering the specified country
    """
    query = {"borders": code.upper()}
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def filter_landlocked(fields: Optional[str]):
    """
    Find all landlocked countries (countries without access to the ocean).

    Args:
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of landlocked countries
    """
    query = {"landlocked": True}
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def filter_by_currency(currency: str, fields: Optional[str]):
    """
    Find countries using a specific currency.

    Args:
        currency: Currency code to filter by
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries using the specified currency
    """
    query = {"currencies.code": currency.upper()}
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def filter_by_language(language: str, fields: Optional[str]):
    """
    Find countries using a specific language.

    Args:
        language: ISO639-1 language code to filter by
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries using the specified language
    """
    query = {"languages.iso639_1": language.lower()}
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def filter_by_translation(translation: str, fields: Optional[str]):
    """
    Find countries that have a translation in a specific language.

    Args:
        translation: Translation language key to filter by
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries with translations in the specified language
    """
    query = {f"translations.{translation}": {"$exists": True}}
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def filter_by_demonym(name: str, fields: Optional[str]):
    """
    Find countries by demonym (name for citizens/inhabitants).

    Args:
        name: Demonym name pattern to search for
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries matching the demonym pattern
    """
    query = {"demonym": {"$regex": name, "$options": "i"}}
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def filter_by_area(
    min: Optional[float],
    max: Optional[float],
    region: Optional[str],
    fields: Optional[str],
):
    """
    Find countries by area range and optionally filtered by region.

    Args:
        min: Minimum area in square kilometers (inclusive)
        max: Maximum area in square kilometers (inclusive)
        region: Optional region name to filter by
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries matching the area criteria
    """
    query: Dict[str, Any] = {}
    area_q: Dict[str, Any] = {}
    if min is not None:
        area_q["$gte"] = min
    if max is not None:
        area_q["$lte"] = max
    if area_q:
        query["areaKm2"] = area_q
    if region:
        query["region"] = region
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def sort_by_density(sort: str, fields: Optional[str]):
    """
    Get countries sorted by population density (population / area).

    Args:
        sort: Sort direction, "asc" for ascending or "desc" for descending
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries sorted by population density
    """
    # compute density on the fly: population / areaKm2
    projection = _build_projection(fields) or {"population": 1, "areaKm2": 1}
    all_docs = await country_collection.find({}, projection).to_list(None)
    all_docs = [convert_mongo_doc(d) for d in all_docs if d.get("areaKm2")]
    all_docs.sort(key=lambda d: d["population"]/d["areaKm2"], reverse=(sort == "desc"))
    return all_docs


async def filter_by_population(
    min: Optional[int],
    max: Optional[int],
    region: Optional[str],
    fields: Optional[str],
):
    """
    Find countries by population range and optionally filtered by region.

    Args:
        min: Minimum population (inclusive)
        max: Maximum population (inclusive)
        region: Optional region name to filter by
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries matching the population criteria
    """
    query: Dict[str, Any] = {}
    pop_q: Dict[str, Any] = {}
    if min is not None:
        pop_q["$gte"] = min
    if max is not None:
        pop_q["$lte"] = max
    if pop_q:
        query["population"] = pop_q
    if region:
        query["region"] = region
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def random_countries(count: int, fields: Optional[str]):
    """
    Get a random selection of countries.

    Args:
        count: Number of random countries to return
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of randomly selected countries
    """
    total = await country_collection.count_documents({})
    count = min(count, total)
    indices = random.sample(range(total), count)
    cursor = country_collection.find({}, _build_projection(fields))
    all_docs = await cursor.to_list(None)
    all_docs = [convert_mongo_doc(doc) for doc in all_docs]
    return [all_docs[i] for i in indices]


async def compare_countries(codes: List[str], fields: Optional[str]):
    """
    Compare multiple countries by their alpha-3 codes.

    Args:
        codes: List of alpha-3 country codes to compare
        fields: Comma-separated list of fields to include in the result

    Returns:
        List of countries matching the provided codes
    """
    query = {"alpha3Code": {"$in": [c.upper() for c in codes]}}
    projection = _build_projection(fields)
    results = await country_collection.find(query, projection).to_list(1000)
    return [convert_mongo_doc(doc) for doc in results]


async def get_meta_regions() -> List[str]:
    """
    Get a list of all unique region names in the database.

    Returns:
        List of region names
    """
    return await country_collection.distinct("region")


async def get_meta_subregions() -> List[str]:
    """
    Get a list of all unique subregion names in the database.

    Returns:
        List of subregion names
    """
    return await country_collection.distinct("subregion")


async def get_meta_languages() -> List[str]:
    # return list of unique iso639_1 codes used
    async def get_meta_languages() -> List[str]:
        """
        Get a list of all unique language codes used in the database.

        Returns:
            List of ISO639-1 language codes
        """
    # return list of unique iso639_1 codes used
    return await country_collection.distinct("languages.iso639_1")


async def get_meta_currencies() -> List[str]:
    """
    Get a list of all unique currency codes used in the database.

    Returns:
        List of currency codes
    """
    return await country_collection.distinct("currencies.code")


