from fastapi import FastAPI, HTTPException

app = FastAPI(title="dev-flow POC")


@app.get("/hello")
def hello_world() -> dict:
    return {"message": "Hello, World!"}


@app.get("/hello/{name}")
def hello_name(name: str) -> dict:
    if len(name) < 2:
        raise HTTPException(
            status_code=400,
            detail="name must be at least 2 characters",
        )
    capitalized = name[0].upper() + name[1:]
    return {"message": f"Hello, {capitalized}!"}
