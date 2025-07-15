from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.github_utils import process_version_update

app = FastAPI()

class ImageUpdate(BaseModel):
  image: str
  version: str

@app.post("/update-image-version")
async def update_image_version(payload: ImageUpdate):
  try:
    process_version_update(payload.image, payload.version)
    return {"status": "success", "message": "Image versions updated and pushed to repo."}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))