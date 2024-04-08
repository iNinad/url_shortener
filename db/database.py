import os

from db.memcache import Memcache
from db.mongodb import MongoDB

# Create an instance of MongoDB using the connection string
# Check if the endpoint is present in an environment variable MONGODB_URI
MONGODB_URI = os.environ.get('MONGODB_URI', "mongodb://localhost:27017/")
mongodb = MongoDB(MONGODB_URI)

# Create an instance of Memcache using the connection string
# Check if the endpoint is present in an environment variable MEMCACHE_URI
MEMCACHE_URI = os.environ.get('MEMCACHE_URI', "localhost:11211")
memcache = Memcache(MEMCACHE_URI)
