# **Streamlit Dashboard Based on BigQuery Mart Table**
[![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![BigQuery](https://img.shields.io/badge/-BigQuery-4285F4?style=flat&logo=google-big-query&logoColor=white)](https://cloud.google.com/bigquery)
[![Visual Crossing](https://img.shields.io/badge/-Visual%20Crossing-00AEEF?style=flat&logo=visualcrossing&logoColor=white)](https://www.visualcrossing.com/)
[![OpenRouter API](https://img.shields.io/badge/-OpenRouter%20API-FF9900?style=flat&logo=openai&logoColor=white)](https://openrouter.ai/)
[![DeepSeek](https://img.shields.io/badge/-DeepSeek-1A73E8?style=flat&logo=deepseek&logoColor=white)](https://deepseek.com/)
[![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions CI/CD](https://img.shields.io/badge/-GitHub%20Actions%20CI%2FCD-24292F?style=flat&logo=githubactions&logoColor=white)](https://docs.github.com/en/actions)
[![Artifact Registry](https://img.shields.io/badge/-Artifact%20Registry-4285F4?style=flat&logo=google-cloud&logoColor=white)](https://cloud.google.com/artifact-registry)
[![Cloud Run](https://img.shields.io/badge/-Cloud%20Run-4285F4?style=flat&logo=google-cloud&logoColor=white)](https://cloud.google.com/run)

This Project aims to create dashboard to visualize all interesting charts that can help weather team on seven next days and that every day you.
Below an example of what you can do with app. You will be able to get suggestion from AI Agent named ``AgentSunAI``.

[![Watch Streamlit App Demo](assets/images/dashboard_ui_screenshot.png)](https://donat-konan33.github.io/assets/videos/demo.mp4)

Click the image above to watch a brief demo of the Streamlit dashboard. The video highlights interactive charts generated from aggregated database values and demonstrates how AgentSunAI offers suggestions on energy consumption, tailored to the projected energy density for each region or department over the next seven days.

---
## **Local Installation**

### 1. Clone the repository:
```bash
git clone https://github.com/donat-konan33/BigQueryStreamlitAnalyticsDashboard.git
cd BigQueryStreamlitAnalyticsDashboard
```
---
### 2. Manage ``.streamlit directory``
**Note :** You need to populate ``.streamlit directory`` with a specific `secrets.toml` file to allow streamlit to connect to your BigQuery Project.

That is like below:

```
# .streamlit/secrets.toml


[gcp_service_account]
type = "service_account"
project_id = "xxx"
private_key_id = "xxx"
private_key = "xxx"
client_email = "xxx"
client_id = "xxx"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "xxx"
```
That supposes you have already got your GCP credential like `SERVICE_ACCOUNT KEY`. For more details hit this [``streamlit docs``](https://docs.streamlit.io/develop/tutorials/databases/bigquery).


### 3. Environment Variables

Important variables needed for app operating:

| Variable             | Description                                                                                  |
|----------------------|----------------------------------------------------------------------------------------------|
| `PROJECT_ID`         | Google Cloud project ID used for BigQuery and other GCP services.                            |
| `OPENROUTER_API_KEY` | API key for accessing OpenRouter services, typically used for AI integrations.               |
| `LOCATION`           | Deployment region or location for cloud resources (e.g., `us-central1`).                     |
| `HOSTNAME`           | Hostname or domain where the application will be deployed or accessed.                       |
| `REPOSITORY`         | Container image repository name (e.g., DockerHub or GCR repository).                         |
| `IMAGE_NAME`         | Name of the container image for the application.                                             |
| `IMAGE_TAG`          | Tag for the container image, often used to specify version (e.g., `latest`, `v1.0.0`).       |
| `IMAGE_FULL_TAG`     | Full reference to the container image including repository, name, and tag.                   |


Now you have the meaning of the variables needed, you have to :
- Populate local variables by following `.env.example` file if you execute locally the App.
- For Production, if You use [``Github Actions``](https://docs.github.com/en/actions/tutorials/deploying-with-github-actions?search-overlay-input=define+environment+variable+on+prod+environment&search-overlay-ask-ai=true) like me you have to assign them as secrets and vars according to your deployment Environment.

As a rule, to define an environment variable in a "prod" environment, follow these steps:

1. Navigate to the main page of your repository on GitHub.
2. Under your repository name, click Settings. If you don't see the "Settings" tab, select the More dropdown menu, then click Settings.
3. In the left sidebar, click Environments.
4. Click on the "prod" environment.
5. Under Environment variables, click Add variable.
6. In the Name field, enter the name of your variable.
7. In the Value field, enter the value for your variable.
8. Click Add variable.

These variables will only be accessible to workflow jobs that reference the "prod" environment and can be accessed using the vars context.

More details: [Managing environments for deployment](https://docs.github.com/en/actions/how-tos/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment).


### 4. Start the Streamlit App in a container with ``Docker compose``

To start the Streamlit app using Docker Compose, run the following command in your terminal:

```bash
docker compose -f docker-compose-streamlit.yml up -d
```

This will build and launch the application in detached mode using the configuration defined in `docker-compose-streamlit.yml`.

---

## **CI/CD workflow Understanding**
We will specially raise this point about ``staging deployment and production deployment``.
In our current case we use :

For ``cd.yml``:

```
name: Deploy to Prod

on:
  workflow_run:
    workflows: ["Continuous Integration Pipeline"]
    types:
      - completed

jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' && github.ref == 'refs/heads/master' }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Deploy Application
        run: ./deploy.sh
```

You surely see our deployment based on the success of ``ci`` step.

However a best Practice would be to create a staging deployment (deploy to test) with its environment into github by defining corresponding and relevant env variables and secrets (important for passing deployment). Once Pull Request (PR) is accepted, the integration ``on master`` will be triggering the deployment to ``prod``.

Let look at this config:

- To ``test APP`` in a test environment (cd-staging.yml):
```
name: Deploy to Staging

on:
  workflow_run:
    workflows: ["Continuous Integration Pipeline"]
    types:
      - completed

jobs:
  deploy-staging:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Deploy to Staging
        run: ./deploy-staging.sh
```

- To deliver the ``final APP`` (cd-prod.yml):
```
name: Deploy to Production

on:
  push:
    branches:
      - master

jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Deploy to Production
        run: ./deploy-prod.sh
```

We guess here ``./deploy-prod.sh and ./deploy-staging.sh`` codes for deployment are available into repository, otherwise codes should be integrated directly in run level for the corresponding deployment.

Finally the we have to create three (3) CI/CD files as
- ci.yml
- cd-staging.yml
- cd-prod.yml

And we'll integrate those soon in a next release of our app. Let's suppose current cd.yml deploy our ``staging app`` to test its behavior.

---

**🚨Important** : The ETLT Data Pipeline source code Using Airbyte, GCS, BigQuery, Dbt and Airflow can be found by hitting this [link](https://github.com/donat-konan33/EtltAirbyteGcsBigQueryDbtAirflow).
