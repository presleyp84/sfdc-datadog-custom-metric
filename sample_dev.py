####### JWT authentication and token extraction ######

from datetime import datetime
from datetime import timedelta
import jwt
import os
import time
import requests

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries


# *** Update these values to match your configuration ***
IS_SANDBOX = False
KEY_FILE = os.environ['SALESFORCE_KEY']
ISSUER = '3MVG9Gmy2zmPB01ph7pKhLznrFjjY9TpOF6KZo56uTiuGKlgIfo_i.jryjRugPuML17hjGrjQYQq76T8N.hgP'
SUBJECT = 'sysuser@sunpower.com.int'

# *******************************************************
DOMAIN = 'test' if IS_SANDBOX else 'login'
#print('Loading private key...')
#with open(KEY_FILE) as fd:
#    private_key = fd.read()

#print('Generating signed JWT assertion...')
claim = {
    'iss': ISSUER,
    'exp': int(time.time()) + 300,
    'aud': 'https://test.salesforce.com',
    'sub': SUBJECT,
}
assertion = jwt.encode(claim, KEY_FILE, algorithm='RS256', headers={'alg':'RS256'})
#print (assertion)
#print('Making OAuth request...')
r = requests.post("https://test.salesforce.com/services/oauth2/token", data = {
    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'assertion': assertion,
})
dict = r.json()
key = list(dict)[0]
token = dict['access_token']

####### lead volume value extraction from endpoint query ######

bt = "Bearer "+token
headers = {'authorization': bt}
prefix = 'https://sunpower--int.sandbox.my.salesforce.com/services/data/v54.0/query?q='

####### Timestamping for dynamic query ######
ts_15m = datetime.now() - timedelta(minutes = 15)
sql_ts_15m = str(ts_15m).replace(" ", "T")
ts_30m = datetime.now() - timedelta(minutes = 30)
sql_ts_30m = str(ts_30m).replace(" ", "T")

query_prefix = "SELECT Count(Id) FROM Lead WHERE RecordTypeId = '0128000000037AKAAY' AND CreatedDate >= "

query1 = query_prefix+sql_ts_15m+"-05:00"+" AND "+ "CreatedDate < "+ sql_ts_30m+"-05:00"+" AND LeadSource = 'Web' AND Source_System__c != null"
print(query1)
url1 = prefix+query1
r1 = requests.get(url1, headers=headers)
#print(r1.json())
dict1 = r1.json()
records1 = dict1['records'][0]
lead_count_recent_value = records1['expr0']
print(sql_ts_15m)
print("expr0 at 15 mins:",lead_count_recent_value)

query2 = query_prefix+sql_ts_15m+"-05:00"+" AND LeadSource = 'Web' AND Source_System__c != null"
print(query2)
url2 = prefix+query2
r2 = requests.get(url2, headers=headers)
#print(r2.json())
dict2 = r2.json()
records2 = dict2['records'][0]
lead_count_total_value = records2['expr0']
print(ts_30m)
print("expr0 at 30 mins:",lead_count_total_value)

####### Datadog custom metric generation ######
     
body_lead_count_recent = MetricPayload(
    series=[
        MetricSeries(
            metric="sfdc.lead.count.recent",
            type=MetricIntakeType(0),
            points=[
                MetricPoint(
                    timestamp=int(datetime.now().timestamp()),
                    value=lead_count_recent_value,
                ),
            ],
            resources=[
                MetricResource(
                    name="sfdc_test",
                    type="host",
                ),
            ],
        ),
    ],
)

body_lead_count_total = MetricPayload(
    series=[
        MetricSeries(
            metric="sfdc.lead.count.total",
            type=MetricIntakeType(0),
            points=[
                MetricPoint(
                    timestamp=int(datetime.now().timestamp()),
                    value=lead_count_total_value,
                ),
            ],
            resources=[
                MetricResource(
                    name="sfdc_test",
                    type="host",
                ),
            ],
        ),
    ],
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MetricsApi(api_client)
    response = api_instance.submit_metrics(body=body_lead_count_recent)
    response1 = api_instance.submit_metrics(body=body_lead_count_total)
    #print(response)
    #print(response1)
