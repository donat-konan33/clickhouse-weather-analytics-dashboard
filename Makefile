.PHONY: build tag push tests

# Launch tests
test_connection:
	poetry run pytest -vv --disable-warnings tests/test_functions.py

build:
	@echo "Building docker image..."
	@docker build -t $(IMAGE_NAME) .

# Tag Image
tag:
	@docker tag $(IMAGE_NAME) $(IMAGE_FULL_TAG)

# Push Image to Artifact Registry
push: tag
	@echo "Pushing docker image..."
	@docker push $(IMAGE_FULL_TAG)

# Deploy image to Cloud Run
deploy:
	@echo "Deploying weather-photovoltaic-app..."
	@gcloud run deploy weather-photovoltaic-app \
		--image=${IMAGE_FULL_TAG} \
		--region=$(LOCATION) \
		--set-env-vars "PROJECT_ID=$(PROJECT_ID)" \
		--set-env-vars "OPENROUTER_API_KEY=$(OPENROUTER_API_KEY)"
		--set-env-vars "PORT=$(PORT)"

# Clean Local Image
clean:
	docker rmi $(IMAGE_NAME) $(IMAGE_FULL_TAG) || true
