from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from rembg import remove
import uvicorn
import io

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Background Remover API")

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    """
    Endpoint to remove background from an uploaded image.
    Returns the image with transparent background (PNG).
    """
    # Validate file type by MIME type and extension
    if not file.content_type.startswith('image/') or file.filename.lower().endswith(('.mp4', '.avi', '.mov')):
        return Response(content=b"Invalid file type. Please upload an image (JPG, PNG).", status_code=400)

    # Read the image file
    input_image = await file.read()
    
    try:
        # Remove background
        # rembg.remove accepts bytes and returns bytes by default
        output_image = remove(input_image)
        
        # Return the processed image
        return Response(content=output_image, media_type="image/png")
    except Exception as e:
        print(f"Error: {e}")
        return Response(content=f"Error processing image: {str(e)}".encode(), status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
