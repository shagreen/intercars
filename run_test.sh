# Easy script for test run in gitlab-ci with coverage report and test exitcode
coverage run -m pytest
pytest_exit_code=$?
coverage report
coverage html
exit $pytest_exit_code
