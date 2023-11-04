import uvicorn
import asyncio
import concurrent.futures

from typing import NoReturn
from fastapi import FastAPI

from realfans_api.tasks import write_events
from realfans_api.utils.colors import bcolors
from realfans_api.routes.user import router as user_router
from realfans_api.utils.cleanup_server import cleanup_server


app = FastAPI()
app.include_router(user_router)

PORT = 8000


async def main(loop) -> NoReturn:
    print(
        f"""
{bcolors.PURPLE}Loading API...{bcolors.END_COLOR}
Visit {bcolors.YELLOW}http://localhost:{PORT}/docs{bcolors.END_COLOR} for documentation
"""
    )
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=False, workers=1)
    cleanup_server()

    # Write the events into the database
    loop.run_in_executor(None, lambda: write_events.execute())
    

    


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()
