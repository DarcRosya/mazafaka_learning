<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

<img src="https://cdn.pfps.gg/pfps/9345-funny-aesthetic-16.png" width="30%" style="position: relative; top: 0; right: 0;" alt="Project Logo"/>

# MAZAFAKA_LEARNING.GIT

<em></em>

<!-- BADGES -->
<img src="https://img.shields.io/github/license/DarcRosya/mazafaka_learning.git?style=flat-square&logo=opensourceinitiative&logoColor=white&color=FF4B4B" alt="license">
<img src="https://img.shields.io/github/last-commit/DarcRosya/mazafaka_learning.git?style=flat-square&logo=git&logoColor=white&color=FF4B4B" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/DarcRosya/mazafaka_learning.git?style=flat-square&color=FF4B4B" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/DarcRosya/mazafaka_learning.git?style=flat-square&color=FF4B4B" alt="repo-language-count">

<em>Built with the tools and technologies:</em>


<img src="https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=flat-square&logo=SQLAlchemy&logoColor=white" alt="SQLAlchemy">
<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=flat-square&logo=FastAPI&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat-square&logo=Docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Pydantic-E92063.svg?style=flat-square&logo=Pydantic&logoColor=white" alt="Pydantic">
<img src="https://img.shields.io/badge/Alembic-4E85A8.svg?style=flat-square&logo=Alembic&logoColor=white" alt="Alembic">
<img src="https://img.shields.io/badge/GitLab_CI-FC6D26.svg?style=flat-square&logo=GitLab&logoColor=white" alt="GitLab CI">

</div>
<br>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Core Endpoints](#core-endpoints)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)

---

## Overview

<em>TaskNest is a task management API built with FastAPI and SQLAlchemy, featuring JWT authentication, email verification, and full CRUD operations for users, tasks, and tags. The project is containerized using Docker and can be deployed locally or via CI/CD pipelines.</em>

---

## Features

- 🔐 **Authentication & Authorization:** User registration and login using JWT (access + refresh tokens).
- 📧 **Email Verification:** Email confirmation for new users.
- 👤 **User Management:** Full CRUD operations for user profiles.
- ✅ **Task Management:** Full CRUD operations for tasks.
- 🏷️ **Tag Management:** Full CRUD operations for tags.
- 🔗 **Flexible Relations:** Assign and remove tags from tasks, filter tasks by tags.
- 🐳 **Containerization:** The project is fully containerized with Docker for easy deployment.
- 🚀 **CI/CD:** GitLab CI/CD pipeline is configured for automatic builds and deployments.
- 📄 **Auto-Documentation:** Interactive API documentation powered by OpenAPI (Swagger UI) and ReDoc.

---

## Project Structure

```sh
└── mazafaka_learning.git/
    ├── Dockerfile
    ├── README.md
    ├── alembic.ini
    ├── docker-compose.yml
    ├── requirements.txt
    └── src
        ├── __init__.py
        ├── api
        ├── config
        ├── main.py
        ├── migrations
        ├── models
        ├── queries
        ├── schemas
        └── utils
```
---

### Core Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| **Authentication** |
| `POST` | `/auth/register` | Register a new user | ❌ |
| `GET` | `/auth/verify` | Verify email via a token from the email | ❌ |
| `POST` | `/auth/login` | Log in and receive a JWT pair | ❌ |
| `POST` | `/auth/refresh` | Refresh the access token | ✅ |
| **Users** |
| `GET` | `/users/me` | Get current user's data | ✅ |
| `PATCH` | `/users/me` | Update current user's data | ✅ |
| `DELETE`| `/users/me` | Delete the current user | ✅ |
| `GET` | `/users/me/tasks`| Get a list of tasks for the current user | ✅ |
| **Tasks** |
| `GET` | `/tasks` | Get a list of all tasks | ✅ |
| `POST` | `/tasks` | Create a new task | ✅ |
| `PATCH` | `/tasks/{task_id}` | Update a task by ID | ✅ |
| `DELETE`| `/tasks/{task_id}` | Delete a task by ID | ✅ |
| `GET` | `/tasks/by_tag` | Filter tasks by tag name | ✅ |
| **Tags** |
| `GET` | `/tags` | Get a list of all tags | ✅ |
| `POST` | `/tags` | Create a new tag | ✅ |
| `PATCH` | `/tags/{tag_id}` | Update a tag by ID | ✅ |
| `DELETE`| `/tags/{tag_id}` | Delete a tag by ID | ✅ |
| **Task-Tag Relations** |
| `PUT` | `/tasks/{task_id}/tags/{tag_id}` | Add a tag to a task | ✅ |
| `DELETE`| `/tasks/{task_id}/tags/{tag_id}` | Remove a tag from a task | ✅ |
| `GET` | `/tags/{task_id}/tags` | Get a list of tags for a task | ✅ |

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pip
- **Container Runtime:** Docker

### Installation

Build mazafaka_learning.git from the source and intsall dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/DarcRosya/mazafaka_learning.git
	❯ cd mazafaka_learning.git
    ```

2. **Set up environment variables:**

    ```sh
    ❯ Create a `.env` file in the root directory by copying from `.env.example`. Fill it with your data (DB credentials, JWT secret key, etc.).
    ```

3.  **Run the project using Docker Compose:**
    This command will build the Docker image, then create and start the API and PostgreSQL database containers.
    ```sh
    ❯ docker-compose up --build
    ```

4.  **Done!** The application will be available at `http://localhost:8000`.

> **A Note on Migrations:**
> **Alembic** is configured for database schema migrations. On the first `docker-compose` run, migrations should be applied automatically. If you change the SQLAlchemy models, create a new migration file with the command:
> ```sh
> ❯ docker-compose exec api alembic revision --autogenerate -m "Your migration message"
> ```
> Then, restart your containers.

### Usage

Run the project with:

**Using [docker](https://www.docker.com/):**
```sh
docker run -it {image_name}
```
**Using [pip](https://pypi.org/project/pip/):**
```sh
python {entrypoint}
```

<div align="right">

[![][back-to-top]](#top)

</div>


[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square


---
