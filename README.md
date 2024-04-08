# URL Shortener API

This is a URL shortener API built using FastAPI framework in Python. It provides endpoints to shorten, delete, fetch original URLs, and redirect to original URLs based on the shortened version.


## Functionality Overview:

The URL shortener application offers a straightforward yet efficient solution for shortening URLs. Users can submit their long URLs via the API and receive shortened versions in response, making them more convenient for sharing and managing. Once a URL is shortened, users can access the original URL by simply using the received shortened URL.

To maintain system efficiency and prevent clutter, shortened URLs have a default expiration time of 72 hours (3 days). Users also have the option to specify a custom expiration time if needed. Once a shortened URL expires, it becomes inaccessible for redirection, ensuring that users don't encounter expired links.

Moreover, the application intelligently handles the scenario where a shortened URL for a given original URL already exists, whether expired or still valid. In such cases, creating a new short URL for the same long URL will simply extend the validity of the existing short URL. This approach minimizes redundancy and optimizes storage usage while ensuring seamless access to shortened URLs for users.


## Database and Caching

This project utilizes MongoDB for the database and Memcache for caching.

### MongoDB

MongoDB is used as the primary database for storing original URLs and their shortened versions. This choice stems from its scalability, enabling horizontal scaling to accommodate potential growth effectively. With MongoDB's flexible data structure and adept handling of read-heavy operations, it efficiently manages URL mappings without necessitating intricate relationships. Furthermore, MongoDB's leader-follower protocol ensures data integrity by facilitating atomic write operations and offers high read throughput. These features align seamlessly with our service requirements, making MongoDB the optimal choice for our database solution.

You can easily get a MongoDB Docker container by running the following command:

```bash
docker run -d --name mongodb-container -p 27017:27017 mongo
```

Ensure that Docker is installed and running before executing this command. This will pull the latest MongoDB image from Docker Hub and run it as a container with port `27017` exposed.

### Memcache

Memcache is employed for caching to enhance performance, particularly during redirection requests. You can obtain a Memcache Docker container by running the following command:

```bash
docker run -d --name memcached-container -p 11211:11211 memcached
```

Again, ensure that Docker is installed and running before executing this command. This will pull the latest Memcache image from Docker Hub and run it as a container with port `11211` exposed.

When a redirection request occurs, the application first checks Memcache for the corresponding original URL to expedite the process and improve overall performance. If the URL is not found in Memcache, it then queries MongoDB for the original URL.

Make sure both MongoDB and Memcache Docker containers are properly configured and accessible to ensure the smooth operation of the URL shortener API.


## Installation

To install and run this application, follow these steps:

1. Clone this repository:

```bash
git clone git@github.com:iNinad/url_shortener.git
```

2. Install dependencies:

```bash
cd <cloned-directory>
pip install -r requirements.txt
```

3. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The server will start running at `http://127.0.0.1:8000/`.

## Endpoints

### Shorten URL

- **Method:** `POST`
- **URL:** `/shorten/`
- **Description:** Shorten a given URL by generating a condensed version. Optionally, specify the expiration time for the short URL.
- **Request Body:**
  - `original_url` (required): The original URL to be shortened.
  - `expiration_in_hrs` (optional): Number of hours until the short URL expires (default: 72 hours).
- **Response:**
  - `short_url`: The shortened URL.

### Delete Shortened URL

- **Method:** `DELETE`
- **URL:** `/shorten/`
- **Description:** Delete a shortened URL.
- **Request Body:**
  - `short_url`: The short URL to be deleted.
- **Response:**
  - `message`: Status message indicating the success of deletion operation.

### Fetch Original URL

- **Method:** `GET`
- **URL:** `/shorten/`
- **Description:** Retrieve the original URL associated with the given short URL.
- **Query Parameter:**
  - `short_url`: The short URL.
- **Response:**
  - `original_url`: The original URL.

### Redirect to Original URL

- **Method:** `GET`
- **URL:** `/{short_url}`
- **Description:** Redirect to the original URL associated with the given short URL.

## Usage

1. Access the base URL (e.g., `http://127.0.0.1:8000/`) to create and delete short URLs.
2. Use Swagger UI available at `http://127.0.0.1:8000/docs` to test the endpoints interactively.
3. Test cases are defined in `tests/test_endpoints.py`.


## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve this project.