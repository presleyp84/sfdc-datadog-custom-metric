# sfdc-datadog-custom-metric
Python code to authenticate Salesforce application endpoint via JWT and query SFDC database and push the output as a custom metric to Datadog

#### Usage
1. Fork the repo.
2. Add salesforce key as a github secret in your forked repo.
3. Update details in custom_metric.py as per your requirement.
4. Run the dockerfile.

#### Docker commands
```
docker build -t sfdc .
docker run -d sfdc <datadog_api_key>
```
