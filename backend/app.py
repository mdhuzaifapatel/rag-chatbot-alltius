from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import answer_query
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask_question(req: Request):
    data = await req.json()
    query = data.get("query", "")

    print(query)
    answer = answer_query(query)
    return {"answer": answer}
