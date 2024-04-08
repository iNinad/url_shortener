from datetime import datetime
from typing import Any, Mapping

from pymongo import MongoClient


class MongoDB:
    def __init__(self, url: str) -> None:
        """
        Initialize a MongoDB client instance.

        Args:
            url (str): The MongoDB connection URL.
        """
        self.client = MongoClient(url)
        self.db = self.client['short_urls']
        self.collection = self.db['short_urls']

    def insert_short_url(self, short_url: str, original_url: str, expiration_date: datetime) -> None:
        """
        Insert a short URL into MongoDB.

        Args:
            short_url (str): The short URL.
            original_url (str): The original URL.
            expiration_date (datetime): The expiration date for the short URL.
        """
        url_doc = {
            'short_url': short_url,
            'original_url': original_url,
            'expiration_date': expiration_date
        }
        self.collection.insert_one(url_doc)

    def find_short_url(self, search_criteria: dict, get_expired_url: bool = False) -> Mapping[str, Any]:
        """
        Find a short URL in MongoDB.

        Args:
            search_criteria (dict): The search criteria.
            get_expired_url (bool): Whether to return an expired short URL or not.

        Returns:
            (dict): A MongoDB document containing the short URL details.

        Raises:
            ValueError: If the short URL is not found, or if it has expired.
        """
        url_data = self.collection.find_one(search_criteria)
        if url_data is None:
            raise ValueError("Short URL not found")
        elif url_data["expiration_date"] < datetime.now():
            if get_expired_url:
                return url_data
            raise ValueError("Short URL has been expired")
        else:
            return url_data

    def delete_short_url(self, short_url: str) -> None:
        """
        Delete a short URL from the MongoDB.

        Args:
            short_url (str): The short URL to delete.
        """
        self.collection.delete_one({'short_url': short_url})

    def update_expiration_date(self, short_url: str, new_expiration_date: datetime) -> None:
        """
        Update the expiration date of a URL in the MongoDB.

        Args:
            short_url (str): The short URL to update.
            new_expiration_date (datetime): The new expiration date.
        """
        self.collection.update_one({'short_url': short_url}, {'$set': {'expiration_date': new_expiration_date}})

    def close_connection(self) -> None:
        """ Close the MongoDB connection. """
        self.client.close()

    def lookup_by_original_url(self, original_url: str) -> Mapping[str, Any] | None:
        """
        Lookup the short URL based on the given original URL.

        Args:
            original_url (str): The original URL to lookup.

        Returns:
            The corresponding short URL data or ValueException if the short URL is not found or expired.
        """
        try:
            url_data = self.find_short_url({"original_url": original_url})
        except ValueError as ve:
            print('Error occurred while searching a short url: ' + str(ve))
            return None
        else:
            return url_data

    def lookup_by_short_url(self, short_url: str) -> Mapping[str, Any]:
        """
        Lookup the short URL based on the given short URL.

        Args:
            short_url (str): The short URL to lookup.

        Returns:
            The corresponding short URL data or ValueException if the short URL is not found or expired.
        """
        return self.find_short_url({"short_url": short_url})
