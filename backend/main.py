from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from agent import Agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


agent = Agent()

@app.get("/")
def home():
    return {
        "message": "Nexus AI Backend Running"
    }

@app.post("/chat")
async def chat(
    question: str = Form(...),
    file: UploadFile = File(None)
):

    file_name = None

    if file:

        file_name = file.filename

        print("FILE RECEIVED:", file_name)

        contents = await file.read()

        with open(file_name, "wb") as f:
            f.write(contents)
    try:
        result = agent.answer(
            question,
            file_name
        )

        import os

        if file_name and os.path.exists(file_name):
            os.remove(file_name)

        return result

    except Exception as e:

        return {
            "tool": "error",
            "answer": str(e)
        }