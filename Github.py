
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
import os
from Solution import get_solution
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
headers = {
    "Accept": "application/json"
}


@app.get("/github-login")
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={client_id}')


@app.get("/github-callback")
async def github_callback(code: str):
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }

    response = requests.post("https://github.com/login/oauth/access_token", params=params, headers=headers)
    response_json = response.json()
    access_token = response_json["access_token"]
    headers.update({"Authorization": f"Bearer {access_token}"})
    return JSONResponse(content=response_json)





def get_user():
    response = requests.get("https://api.github.com/user", headers=headers)
    user = response.json()
    username = user["login"]
    return username


@app.get("/user/repos")
async def get_repo():
    user = get_user()
    response = requests.get(f"https://api.github.com/users/{user}/repos", headers=headers)
    repo = response.json()
    return repo


@app.get("/user/repos/{repo_name}")
async def push(repo_name: str, link: str):
    filename, data = get_solution(link)

    user = get_user()

    response = requests.get(f"https://api.github.com/users/{user}/repos", headers=headers)
    repo = response.json()
    repo_names = [r["name"] for r in repo]
    print(repo_names)
    if repo_name not in repo_names:
        return JSONResponse(status_code=404, content={"message": "Repository not found"})

    response = requests.put(f"https://api.github.com/repos/{user}/{repo_name}/contents/{filename}",
                            headers=headers,
                            json={
                                "message": "Add file",
                                "content": data,
                            })
    os.remove(filename)
    return response.json()
