build_and_deploy:
	@echo "Building and deploying app"
	@buildozer android debug deploy run

run_examples:
	@echo "Running examples"
	@pipenv run python /usr/share/kivy-examples/demo/kivycatalog/main.py

run_adb:
	@echo "Connecting to device via USB"
	@export PATH=$PATH:/home/admin1/.buildozer/android/platform/android-sdk/platform-tools/adb
	@adb logcat

run_adb_filtered:
	@echo "Connecting to device via USB"
	@export PATH=$PATH:/home/admin1/.buildozer/android/platform/android-sdk/platform-tools/adb
	@adb logcat | grep -E "python|myservice"

run:
	# @rm -rf ./bin/*
	@make build_and_deploy
	@make run_adb_filtered

run_full_logs:
	@rm -rf ./bin/*
	@make build_and_deploy
	@make run_adb