from fastapi import FastAPI
from fastapi.responses import FileResponse

from api import endpoints

# Initialize FastAPI app
app = FastAPI(title="URL Shortener", swagger_ui_parameters={"defaultModelsExpandDepth": -1})

# Include the endpoints from 'api' package
app.include_router(endpoints.router)


@app.get("/", include_in_schema=False,
         description="The method responds with the `index.html` which is located in the `static` directory.")
async def root():
    """
    This is a root endpoint of the server which responds with the index.html, placed in the static directory.

    Returns:
            FileResponse: a FastAPI response class for files. It reads the file from the `static/index.html`
            and sends that directly as the response.
    """
    return FileResponse('static/index.html')

