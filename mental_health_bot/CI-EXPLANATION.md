# CI/CD Pipeline Explanation

This project uses GitHub Actions to create a simple CI/CD pipeline. The pipeline is defined in the `.github/workflows/ci.yml` file and it runs on every push or pull request to the `main` branch.

The pipeline has two jobs:

## 1. `test`

This job runs on an `ubuntu-latest` runner and it performs the following steps:

1.  **Checkout code:** It checks out the code from the repository.
2.  **Set up Python:** It sets up a Python 3.9 environment.
3.  **Install dependencies:** It installs the Python dependencies from the `requirements.txt` file.
4.  **Test with pytest:** It runs the tests using `pytest`. Currently, there are no tests, so it just checks if the Python files compile.

## 2. `build`

This job runs on an `ubuntu-latest` runner and it depends on the `test` job, which means it will only run if the `test` job completes successfully. It performs the following steps:

1.  **Checkout code:** It checks out the code from the repository.
2.  **Login to GitHub Container Registry:** It logs in to the GitHub Container Registry using the `GITHUB_TOKEN` secret.
3.  **Build and push:** It builds the Docker image and pushes it to the GitHub Container Registry. The image will be tagged with the `latest` tag.
