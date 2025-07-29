from fastapi import FastAPI
from src.api import include_routers
#### TASK NET PROJECT #####
app = FastAPI(title="FastApi - TaskNet")
include_routers(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# uvicorn src.main:app --reload


#  from __future__ import annotations так же когда работаешь с relationship.
# опционально сделать логику с выдачей токена лишь после потверждения email

# GIGACHAD
# SIGMA.MALE@nobitches.com
# SKIBIDIBOSS


# bighorse
# tiny