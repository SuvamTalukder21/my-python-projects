from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from app.crud import (get_all_countries, get_country_by_code, search_countries,
                      filter_by_border, filter_landlocked, filter_by_currency,
                      filter_by_capital, filter_by_region, filter_by_subregion,
                      filter_by_language, filter_by_translation, filter_by_demonym,
                      filter_by_area, sort_by_density, filter_by_population,
                      random_countries, compare_countries, get_meta_regions,
                      get_meta_subregions, get_meta_languages, get_meta_currencies)

router = APIRouter(prefix="/v1", tags=["countries"])


# Core Country Endpoints
@router.get("/all")
async def all_countries(
    fields: Optional[str] = None,
    sort: Optional[str] = None,
    unMember: Optional[bool] = None,
    independent: Optional[bool] = None,
    limit: int = Query(100, ge=1, le=1000),
    skip: int = Query(0, ge=0),
):
    """
    Retrieve a list of all countries with optional filtering and sorting.

    **Parameters:**
        fields: Comma-separated list of fields to include in the response
        sort: Field to sort by
        unMember: Filter by UN membership status (true/false)
        independent: Filter by independence status (true/false)
        limit: Maximum number of results to return (1-1000, default: 100)
        skip: Number of results to skip for pagination (default: 0)

    **Returns:**
        List of country objects matching the criteria
    """
    return await get_all_countries(fields, sort, unMember, independent, limit, skip)


@router.get("/id/{id}")
async def country_by_id(id: str, fields: Optional[str] = None):
    """
    Retrieve a specific country by its unique ID.

    Parameters:
        id: Unique identifier for the country
        fields: Comma-separated list of fields to include in the response

    Returns:
        Country object or 404 if not found
    """
    country = await get_country_by_code(id, fields)
    if not country:
        raise HTTPException(404, "Country not found")
    return country


@router.get("/alpha/{code}")
async def country_by_code(code: str, fields: Optional[str] = None):
    """
    Retrieve a specific country by its alpha code (2 or 3 letters).

    Parameters:
        code: Alpha-2 or Alpha-3 country code
        fields: Comma-separated list of fields to include in the response

    Returns:
        Country object or 404 if not found
    """
    country = await get_country_by_code(code, fields)
    if not country:
        raise HTTPException(404, "Country not found")
    return country


# Search & Filter Endpoints
@router.get("/search")
async def countries_search(
    q: str = Query(..., description="Partial or full country name"),
    fields: Optional[str] = None
):
    """
    Search countries by name.

    Parameters:
        q: Partial or full country name to search for
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries matching the search query
    """
    return await search_countries(q, fields)


@router.get("/name/{countryName}")
async def country_by_name(countryName: str, fields: Optional[str] = None):
    """
    Find a country by its exact name.

    Parameters:
        countryName: Exact country name
        fields: Comma-separated list of fields to include in the response

    Returns:
        Country object matching the name or empty array if not found
    """
    return await search_countries(countryName, fields, exact=True)


@router.get("/capital/{capital}")
async def countries_by_capital(capital: str, fields: Optional[str] = None):
    """
    Find countries by their capital city.

    Parameters:
        capital: Name of the capital city
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries with the matching capital
    """
    return await filter_by_capital(capital, fields)


# Geographical Endpoints
@router.get("/region/{region}")
async def countries_by_region(region: str, fields: Optional[str] = None):
    """
    Filter countries by geographical region.

    Parameters:
        region: Region name
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries in the specified region
    """
    return await filter_by_region(region, fields)


@router.get("/subregion/{subregion}")
async def countries_by_subregion(subregion: str, fields: Optional[str] = None):
    """
    Filter countries by geographical subregion.

    Parameters:
        subregion: Subregion name
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries in the specified subregion
    """
    return await filter_by_subregion(subregion, fields)


@router.get("/bordering/{code}")
async def countries_bordering(code: str, fields: Optional[str] = None):
    """
    Get all countries that share a border with the specified country.

    Parameters:
        code: Alpha-3 code of the country
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries bordering the specified country
    """
    return await filter_by_border(code, fields)


@router.get("/landlocked")
async def landlocked_countries(fields: Optional[str] = None):
    """
    Get all landlocked countries.

    Parameters:
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of landlocked countries
    """
    return await filter_landlocked(fields)


# Cultural/Linguistic Endpoints
@router.get("/currency/{currency}")
async def countries_by_currency(currency: str, fields: Optional[str] = None):
    """
    Find countries that use a specific currency.

    Parameters:
        currency: Currency code
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries using the specified currency
    """
    return await filter_by_currency(currency, fields)


@router.get("/lang/{language}")
async def countries_by_language(language: str, fields: Optional[str] = None):
    """
    Find countries that use a specific language.

    Parameters:
        language: ISO639-1 language code
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries using the specified language
    """
    return await filter_by_language(language, fields)


@router.get("/translation/{translation}")
async def countries_by_translation(translation: str, fields: Optional[str] = None):
    """
    Find countries that have a translation in a specific language.

    Parameters:
        translation: Translation language key
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries with translations in the specified language
    """
    return await filter_by_translation(translation, fields)


@router.get("/demonym/{name}")
async def countries_by_demonym(name: str, fields: Optional[str] = None):
    """
    Find countries by their demonym (name for citizens/inhabitants).

    Parameters:
        name: Demonym name pattern to search for
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries with matching demonym
    """
    return await filter_by_demonym(name, fields)


# Statistical Endpoints
@router.get("/area")
async def countries_by_area(
    min: Optional[float] = Query(None, ge=0),
    max: Optional[float] = Query(None, ge=0),
    region: Optional[str] = None,
    fields: Optional[str] = None,
):
    """
    Filter countries by area range.

    Parameters:
        min: Minimum area in square kilometers
        max: Maximum area in square kilometers
        region: Region name to further filter results
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries within the specified area range
    """
    return await filter_by_area(min, max, region, fields)


@router.get("/density")
async def countries_density(
    sort: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    fields: Optional[str] = None
):
    """
    Get countries sorted by population density.

    Parameters:
        sort: Sort direction, "asc" (default) or "desc"
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries sorted by population density
    """
    return await sort_by_density(sort, fields)


@router.get("/population")
async def countries_by_population(
    min: Optional[int] = Query(None, ge=0),
    max: Optional[int] = Query(None, ge=0),
    region: Optional[str] = None,
    fields: Optional[str] = None
):
    """
    Filter countries by population range.

    Parameters:
        min: Minimum population
        max: Maximum population
        region: Region name to further filter results
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of countries within the specified population range
    """
    return await filter_by_population(min, max, region, fields)


# Special Feature Endpoints
@router.get("/countries/random")
async def random_country(count: int = Query(1, ge=1, le=100), fields: Optional[str] = None):
    """
    Get random countries.

    Parameters:
        count: Number of random countries to return (1-100, default: 1)
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of random country objects
    """
    return await random_countries(count, fields)

@router.get("/compare")
async def compare(codes: str = Query(..., description="Comma-separated codes"), fields: Optional[str] = None):
    """
    Compare multiple countries.

    Parameters:
        codes: Comma-separated list of alpha-3 country codes to compare
        fields: Comma-separated list of fields to include in the response

    Returns:
        List of country objects for comparison
    """
    code_list = codes.split(",")
    return await compare_countries(code_list, fields)


# Metadata Endpoints
@router.get("/meta/regions")
async def meta_regions():
    """
    Get a list of all available regions.

    Returns:
        Array of region names
    """
    return await get_meta_regions()


@router.get("/meta/subregions")
async def meta_subregions():
    """
    Get a list of all available subregions.

    Returns:
        Array of subregion names
    """
    return await get_meta_subregions()


@router.get("/meta/languages")
async def meta_languages():
    """
    Get a list of all available language codes.

    Returns:
        Array of ISO639-1 language codes
    """
    return await get_meta_languages()


@router.get("/meta/currencies")
async def meta_currencies():
    """
    Get a list of all available currency codes.

    Returns:
        Array of currency codes
    """
    return await get_meta_currencies()


# # Define the API route for a specific country by code
# @router.get("/alpha/{code}")
# async def read_country(code: str):
#     country = await get_country_by_code(code=code)
#     if not country:
#         raise HTTPException(status_code=404, detail="Country not found")
#     return country


