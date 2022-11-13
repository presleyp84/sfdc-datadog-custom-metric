# sfdc-datadog-custom-metric
Python code to authenticate via JWT and query SFDC database and push custom metric to Datadog

##Usage

Fork the repo.
add salesforce key as a github secret in your forked repo.
update details in custom_metric.py as per your requirement.
run the dockerfile.

###Docker commands

docker build -t sfdc .
docker run -d sfdc <datadog_api_key>
