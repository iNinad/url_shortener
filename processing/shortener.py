from datetime import datetime, timedelta
from typing import Union

from db.memcache import Memcache
from db.mongodb import MongoDB
from processing.encoder import generate_encoded_string


class URLShortener:
    def __init__(self, mongodb: MongoDB, memcache: Memcache) -> None:
        """
        Initialize URLShortener with MongoDB and Memcache instances.

        Args:
            mongodb (MongoDB): MongoDB instance.
            memcache (Memcache): Memcache instance.
        """
        self.mongodb = mongodb
        self.memcache = memcache

    def generate_short_url(self, original_url: str, expiration_days_in_hrs: int = 72) -> str:
        """
        Generate a short URL and return it.

        A new short URL is generated, stored in MongoDB and Memcache,
        and then returned. The new short URL will expire after `expiration_days_in_hrs` hours.

        Args:
            original_url (str): Original URL to shorten.
            expiration_days_in_hrs (int, optional): Number of hours until the short URL expires.

        Returns:
            str: A short URL string.
        """
        expiration_date = datetime.now() + timedelta(
            hours=expiration_days_in_hrs)  # Set the expiration date

        expiration_in_secs = expiration_days_in_hrs * 60 * 60  # Convert hours to seconds

        existing_url_data = self.mongodb.lookup_by_original_url(original_url)
        if existing_url_data:
            self.mongodb.update_expiration_date(existing_url_data['short_url'], expiration_date)
            # Return existing short URL if found
            return existing_url_data['short_url']

        short_url = generate_encoded_string()  # Generate a new short URL

        # Insert new short URL into MongoDB and Memcache
        self.mongodb.insert_short_url(short_url, original_url, expiration_date)
        self.memcache.set_cache(short_url, original_url, expiration_in_secs)

        return short_url

    def delete_short_url(self, short_url: str) -> Union[str, Exception]:
        """
        Delete a short URL from the database.

        Raises a ValueError if the short URL does not exist or has already expired.

        Args:
            short_url (str): Short URL to delete.
        Returns:
            str: Success message string.
        """
        try:
            # Check if the short URL is in MongoDB
            _ = self.mongodb.lookup_by_short_url(short_url)
            # Delete the short URL from MongoDB and Memcache
            self.mongodb.delete_short_url(short_url)
            self.memcache.delete_cache(short_url)
        except Exception as e:
            print('Error occurred while deleting a short URL: ', e)
            raise

        return "Short URL deleted successfully"

    def get_original_url(self, short_url: str) -> Union[str, Exception]:
        """
        Retrieve the original URL from a short URL.

        It first attempts to fetch the original URL from Memcache. If not found,
        it looks up MongoDB. If the short URL exists and has not expired,
        the original URL is cached in Memcache and returned.

        Args:
            short_url (str): Short URL.
        Returns:
            str: Original URL string.
        """
        # Try to get the original URL from Memcache
        original_url = self.memcache.get_cache(short_url)
        if not original_url:
            # If not in Memcache, try to get it from MongoDB
            try:
                url_data = self.mongodb.lookup_by_short_url(short_url)
            except Exception as e:
                print('Error occurred while getting an original URL: ', e)
                raise

            # Get the original URL and cache it in Memcache
            original_url = url_data["original_url"]
            self.memcache.set_cache(short_url, original_url,
                                    expiration_time=(url_data["expiration_date"] - datetime.now()).
                                    total_seconds())

        return original_url
