# Welcome to this Project
 This Project aims to create dashboard to visualize all interesting charts that can help weather team on seven next days and that every day you.

Below an example of what you can do with app. You will be able to get suggestion from AI Agent named `AgentSunAI`
![watch video](video.mp4)

---

## CI/CD workflow
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
