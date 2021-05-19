build_and_deploy:
	@echo "Building and deploying app"
	@buildozer android debug deploy run

run_examples:
	@echo "Running examples"
	@pipenv run python /usr/share/kivy-examples/demo/kivycatalog/main.py