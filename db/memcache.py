import memcache as mc


class Memcache:
    def __init__(self, url: str) -> None:
        """
        Initialize a Memcache client instance.

        Args:
            url (str): The Memcache connection URL.
        """
        self.client = mc.Client([url])

    def set_cache(self, key: str, value: str, expiration_time: int) -> None:
        """
        Set a key-value pair in Memcache with an expiration time.

        Args:
            key (str): The key to set.
            value (str): The value to set.
            expiration_time (int): The key-value pair expiration time.
        """
        self.client.set(key, value, time=expiration_time)

    def get_cache(self, key: str) -> str:
        """
        Retrieve a value from Memcache based on its key.

        Args:
            key (str): The key of the value.

        Returns:
            The value corresponding to the key, or None if the key doesn't exist.
        """
        return self.client.get(key)

    def delete_cache(self, key: str) -> None:
        """
        Delete a key-value pair in Memcache.

        Args:
            key (str): The key of the value to delete.
        """
        self.client.delete(key)
