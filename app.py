from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import subprocess
import json
import os
import tempfile

app = FastAPI()

@app.post("/ocr/")
async def ocr_passport(file: UploadFile = File(...)):
    try:
        # Create a temporary file to store the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        # Run the OCR script as a subprocess
        result = subprocess.run(
            ["python", "C:\\Users\\ALNOUR\\OCR-Passport-Reader\\src\\main.py", "--image_path", temp_file_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the output as JSON
        ocr_result = json.loads(result.stdout)

        # Delete the temporary file
        os.unlink(temp_file_path)

        return JSONResponse(content=ocr_result)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"OCR process failed: {e.stderr}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse OCR output")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8080)