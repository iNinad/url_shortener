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

### Memcache

Memcache is employed for caching to enhance performance, particularly during redirection requests. 
When a redirection request occurs, the application first checks Memcache for the corresponding original URL to expedite the process and improve overall performance. If the URL is not found in Memcache, it then queries MongoDB for the original URL.


## Installation

There are two approaches to install and run the URL shortener application:

### Approach 1: Using Docker Compose (Recommended)

Docker Compose simplifies the setup process by bundling all components into containers. Here's how to proceed:

1. Ensure Docker is installed on your machine.

2. Clone this repository:

    ```bash
    git clone git@github.com:iNinad/url_shortener.git
    ```

3. Navigate to the cloned directory:

    ```bash
    cd url_shortener
    ```

4. Run the following command to start the application:

    ```bash
    docker-compose up --build -d
    ```

    This command will pull the necessary Docker images, build the application image, and start all containers. The URL shortener application will be accessible at [http://localhost:8000/](http://localhost:8000/).

### Approach 2: Manual Setup

If you prefer manual setup or customization, follow these steps:

1. Clone this repository:

    ```bash
    git clone git@github.com:iNinad/url_shortener.git
    ```

2. Navigate to the cloned directory:

    ```bash
    cd url_shortener
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

    The server will start running at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Regardless of the approach chosen, the URL shortener application will be up and running, allowing users to shorten, delete, fetch original URLs, and redirect to original URLs effortlessly.


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