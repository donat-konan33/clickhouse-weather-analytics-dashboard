.PHONY: build tag push

build:
	docker build -t $(IMAGE_NAME) .

# Tag Image
tag:
	docker tag $(IMAGE_NAME) $(IMAGE_FULL_TAG)

# Push Image to Artifact Registry
push: tag
	docker push $(IMAGE_FULL_TAG)

# Clean Local Image
clean:
	docker rmi $(IMAGE_NAME) $(IMAGE_FULL_TAG) || true
