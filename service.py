import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field


class ProjectData(BaseModel):
    repos: int = Field(ge=0)
    stars: int = Field(ge=0)
    followers: int = Field(ge=0)
    recent_commits: int = Field(ge=0)
    project_type: int = Field(ge=0, le=4)
    has_readme: bool
    has_demo: bool
    has_tests: bool


app = FastAPI(title="Project scoring")
model = joblib.load("model.pkl")


@app.post("/score")
def score(data: ProjectData):
    features = [
        data.repos,
        data.stars,
        data.followers,
        data.recent_commits,
        data.project_type,
        data.has_readme,
        data.has_demo,
        data.has_tests,
    ]
    probability = model.predict_proba([features])[0][1].item()
    strong_project = probability >= 0.6
    return {"strong_project": strong_project, "probability": probability}
