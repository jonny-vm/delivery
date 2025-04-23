import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette import status

from delivery.api.Adapters.Http import controller

description = """API сервиса доставки (delivery)"""


def create_app() -> FastAPI:
    app = FastAPI(
        title="Сервис доставки",
        description=description,
        openapi_tags=controller.tags_metadata,
    )

    app.add_exception_handler(
        Exception,
        lambda _, exc: JSONResponse(
            {"error": f"{type(exc).__name__}: {exc}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
    )

    app.include_router(controller.router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
