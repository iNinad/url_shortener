import validators
from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.responses import RedirectResponse
from pydantic import AnyUrl, ValidationError

from db.database import mongodb, memcache
from processing.shortener import URLShortener

# Create the instance of application's router
router = APIRouter(tags=["APIs for the URL Shortener"])

# Initialize URL Shortener with MongoDB and Memcache as storage
shortener = URLShortener(mongodb, memcache)


@router.post("/shorten/", summary="Shorten a given URL",
             description="This API method shortens a provided URL by creating a condensed version. "
                         "It accepts the original URL to be shortened and an optional parameter "
                         "specifying the number of hours until the short URL expires, defaulting to 72 hours (3 days). "
                         "It returns a dictionary containing the shortened URL.")
async def shorten_url(request: Request,
                      original_url: AnyUrl = Body(..., description="The original URL to be shortened"),
                      expiration_in_hrs: int = Body(72,
                                                    description="Number of hours until the short URL expires", gt=0)):
    """
    Shorten a given URL.

    Args:
        request (Request): The incoming request object.
        original_url (AnyUrl): The original URL to be shortened.
        expiration_in_hrs (int, optional): Number of hours until the short URL expires, default is 72.

    Returns:
        dict: A dictionary containing the shortened URL.
    """
    # Validate the provided URL
    try:
        validators.url(str(original_url))
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid URL provided")

    short_url = shortener.generate_short_url(str(original_url), expiration_in_hrs)
    complete_short_url = f'{request.base_url}{short_url}'
    return {"short_url": complete_short_url}


@router.delete("/shorten/", summary="Delete a shortened URL",
               description="This API method deletes a shortened URL. It expects a request body containing "
                           "the short URL to be deleted. It returns a status message indicating the success of the "
                           "deletion operation. If the short URL does not exist in the system or has expired, "
                           "it raises an HTTPException.")
async def delete_short_url(short_url: dict = Body(...,
                                                  example={"short_url": "your_short_url"},
                                                  description="The short URL to be deleted")):
    """
    Delete a shortened URL.

    Args:
        short_url (dict): The request body containing the short URL to be deleted.

    Returns:
        dict: The status message.

    Raises:
        HTTPException: If the short URL does not exist in the system or is expired.
    """
    try:
        # Extract short URL from the request body
        short_url_value = short_url.get("short_url")
        if not short_url_value:
            raise HTTPException(status_code=400, detail="The request body must contain 'short_url' key")

        # Extract short URL value from the path
        short_url_value = short_url_value.rsplit('/', 1)[-1]

        # Delete the short URL
        shortener.delete_short_url(short_url_value)

        # Return success message
        return {"message": "Short URL deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/shorten/", summary="Get an original URL",
            description="This API method retrieves the original URL associated with the given short URL. "
                        "It expects a request body containing the short URL. It returns a dictionary containing "
                        "the original URL. If the short URL does not exist in the system or has expired, "
                        "it raises an HTTPException.")
async def fetch_original_url(short_url: str):
    """
    Get the original URL mapped to the given short URL.

    Args:
        short_url (str): The short URL.

    Returns:
        dict: A dictionary containing the original URL

    Raises:
        HTTPException: If the short URL does not exist in the system or is expired.
    """
    try:
        short_url = short_url.rsplit('/', 1)[-1]
        original_url = shortener.get_original_url(short_url)
        return {"original_url": original_url}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{short_url}", include_in_schema=False,
            description="This API method redirects to the original URL associated with the given short URL. "
                        "It expects the short URL as part of the request URL path. If the short URL exists "
                        "in the system and is not expired, it returns a redirection response to the original URL. "
                        "If the short URL does not exist or has expired, it raises an HTTPException.")
async def redirect_to_original_url(short_url: str):
    """
    Redirect to the original URL based on the short URL.

    Args:
        short_url (str): The short URL used for redirection.

    Returns:
        RedirectResponse: A redirection response to be routed to the original URL.

    Raises:
        HTTPException: If the short URL does not exist in the system or is expired.
    """
    try:
        original_url = shortener.get_original_url(short_url)
        return RedirectResponse(url=original_url)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
