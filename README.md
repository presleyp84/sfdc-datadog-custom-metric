# sfdc-datadog-custom-metric
Python code to authenticate via JWT and query SFDC database and push custom metric to Datadog

#### Usage

1.Fork the repo.
2. Add salesforce key as a github secret in your forked repo.
3. Update details in custom_metric.py as per your requirement.
4. Run the dockerfile.

#### Docker commands

1. docker build -t sfdc .
2. docker run -d sfdc <datadog_api_key>
