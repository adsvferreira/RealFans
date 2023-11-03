import uvicorn
from typing import NoReturn
from fastapi import FastAPI

from realfans_api.utils.colors import bcolors
from realfans_api.utils.cleanup_server import cleanup_server
from realfans_api.routes.helloworld import router as hello_world_router


app = FastAPI()
app.include_router(hello_world_router)

PORT = 8000

def main() -> NoReturn:
    print(
        f"""
{bcolors.PURPLE}Loading API...{bcolors.END_COLOR}
Visit {bcolors.YELLOW}http://localhost:{PORT}/docs{bcolors.END_COLOR} for documentation
"""
    )
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=False, workers=1)
    cleanup_server()

if __name__ == "__main__":
    main()