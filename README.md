# sfdc-datadog-custom-metric
Python code to authenticate Salesforce application endpoint via JWT and query SFDC database and push the output as a custom metric to Datadog

#### Prerequisites
<details>
<summary style="font-size:14px">View Prerequisites here</summary>
<p>
Create an RSA x509 private key/certification pair

```
openssl req -x509 -sha256 -nodes -days 36500 -newkey rsa:2048 -keyout salesforce.key -out salesforce.crt
```

The private key (.key) will be used to sign the JWT claim generated by your code.  The certificate (.crt) will be uploaded to Salesforce to validate your signed JWT assertions.

## Salesforce Application creation

1. Login to salesforce.
1. Go to setup area (gear in the nav in the top right)
1. In the side nav, go to _Apps_ > _App Manager_
   1. Click _New Connect App_
   1. In the _Basic Information_ section, populate the required fields.  The values are for book keeping only and are not part of using the API.
   1. In the _API (Enable OAuth Settings)_ section:
      1. Check _Enable OAuth Settings_
      1. _Callback URL_ is unused in the JWT flow but a value is required nonetheless.  Use "http://localhost/" or some other dummy host.
      1. Check _Use digital signatures_.  Upload the _salesforce.crt_ that was generated earlier.
      1. For _Selected OAuth Scopes_, add _Access and manage your data (api)_ and _Perform requests on your behalf at any time (refresh_token, offline_access)_
   1. Click _Save_.  If there are any errors, you have to re-upload _salesforce.crt_.
1. On the resulting app page, click _Manage_.
   1. Click _Edit Policies_.
   1. In the _OAuth policies_ section, change _Permitted Users_ to _Admin approved users are pre-authorized_.
   1. Click _Save_.
1. Back on the app page again, in the _Profiles_ section, click _Manage Profiles_.
   1. On the _Application Profile Assignment_ page, assign the user profiles that will have access to this app.


## OAuth Access Configuration

To use the API, the RSA private key and the _Consumer Key_ (aka client ID) from the Salesforce application are needed.

1. The private key is the key that was generated in the _Prequisite_ section above.
1. To get the Salesforce application _Consumer Key_, do the following
   1. Login to salesforce.
   1. Go to setup area (gear in the nav in the top right)
   1. In the side nav, go to _Apps_ > _App Manager_
   1. In the list, find the application that you created in the _App Creation_ section above
   1. From the drop down in the application's row, click _View_
   1. The _Consumer Key_ is in the _API (Enable OAuth Settings)_ section.
</p>
</details>

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
