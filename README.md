# **Streamlit Dashboard Based on BigQuery Mart Table**
---

 This Project aims to create dashboard to visualize all interesting charts that can help weather team on seven next days and that every day you.

Below an example of what you can do with app. You will be able to get suggestion from AI Agent named `AgentSunAI`
[🎥 Watch Streamlit App Demo](https://donat-konan33.github.io/assets/videos/demo.mp4)

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
For more details hit this [``streamlit docs``](https://docs.streamlit.io/develop/tutorials/databases/bigquery).

---



## **CI/CD workflow**
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

## Environment Variables

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

For Production, if You use Github Actions like me you have to assign them as secrets according to your Prod Environment.

---

**Important** : The ETLT Data Pipeline source code Using Airbyte, GCS, BigQuery, Dbt and Airflow can be found by hitting this [link](https://github.com/donat-konan33/EtltAirbyteGcsBigQueryDbtAirflow).
