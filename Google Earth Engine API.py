# Databricks notebook source
# MAGIC %md
# MAGIC # Google Earth Engine API
# MAGIC
# MAGIC In order to connect to the Google Earth Engine API, we first need to create a Google Cloud project. Uses of the Google Earth Engine API will go through that project and will charge it instead of this FSDH Workspace.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. [Create a Google Cloud Project](https://developers.google.com/workspace/guides/create-project)
# MAGIC Follow the link for instructions on how to create a Google Cloud Project.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Enable the Google Earth Engine API
# MAGIC Once your project is created and selected, in the navigation bar, click on "APIs & Services":
# MAGIC
# MAGIC ![pic1](/files/tables/APIS.png)
# MAGIC
# MAGIC Then click on "Enable APIs & Services":
# MAGIC
# MAGIC ![pic2](/files/tables/Enable.png)
# MAGIC
# MAGIC Search for "Google Earth Engine API", it should then appear in the search results. Click on it, then click on "Enable".

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Create a Service account and obtain a private key.
# MAGIC Once you have enabled the Earth Engine API in your project, open the navigation menu and click on "IAM & Admin":
# MAGIC
# MAGIC ![](/files/tables/IAM.png)
# MAGIC
# MAGIC Then click on "Service Accounts":
# MAGIC
# MAGIC ![](/files/tables/Service.png)
# MAGIC
# MAGIC Then create a new service account:
# MAGIC
# MAGIC ![](/files/tables/Create.png)
# MAGIC
# MAGIC Enter the necessary information (name, ID, description) in the first step, then in the second step, select the "Google Earth Engine Resource Admin" role for your service account:
# MAGIC
# MAGIC ![](/files/tables/EEAdmin.png)
# MAGIC
# MAGIC Then, skip the 3rd step and create your service account by clicking on "Done". This should bring you back to the list of all service accounts and you should see the service account you just created listed. Click on it, then click on the "Keys" tab:
# MAGIC
# MAGIC ![](/files/tables/Keys.png)
# MAGIC
# MAGIC Click on "Add Key" and "Create new key", and select the JSON format for your key:
# MAGIC
# MAGIC ![](/files/tables/NewKey.png)
# MAGIC
# MAGIC This will automatically create a key and download it. Make sure you keep this key.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Register your cloud project
# MAGIC
# MAGIC Navigate to [this registering link](https://code.earthengine.google.com/register) and sign-in using the same google account you use for Google Cloud.
# MAGIC
# MAGIC Select "Use with a Cloud Project"
# MAGIC
# MAGIC Select "Paid" or "Unpaid usage" depending on your personal needs and role. In our case, we will select "Unpaid usage". It will prompt you to select a project type, select "Government".
# MAGIC
# MAGIC Select "Choose an existing cloud project" and select the project you have enabled Google Earth Engine API in.
# MAGIC
# MAGIC Finally, review the information you have given and confirm.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Install the Google Earth Engine Python SDK
# MAGIC
# MAGIC There are two ways to do so. To install the python package only within your notebook, run the following in a python cell:
# MAGIC
# MAGIC ```
# MAGIC %pip install earthengine-api
# MAGIC ```
# MAGIC
# MAGIC Upon the success of running this line, skip to the next step. If instead you want to install the Google Earth Engine Python SDK on the cluster, open the navigation bar on Databricks, and click "Compute". Select the cluster you want to install the package on, then click on libraries:
# MAGIC
# MAGIC ![](/files/tables/libraries.png)
# MAGIC
# MAGIC Then click on "Install new":
# MAGIC
# MAGIC ![](/files/tables/install.png)
# MAGIC
# MAGIC In the pop-up menu, select PyPI, and in the "package name" field, enter "earthengine-api", then click "Install". Once you start your cluster, it will install the library and it will be available on all notebooks that are attached to this cluster.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Using Google Earth Engine API
# MAGIC
# MAGIC Begin by uploading the private key we created from step 3. You can do so by either uploading to your FSDH storage, or you can upload directly to Databricks. Take note of where your key file is located, then use the following Python code to initiate a session:

# COMMAND ----------

# MAGIC %pip install earthengine-api

# COMMAND ----------

# MAGIC %md
# MAGIC ### Using a private key uploaded through the Databricks File Upload

# COMMAND ----------

import ee

# Enter the email associated with your service account created in step 3:
service_account = 'my-service-account@...gserviceaccount.com'
# In our case:
service_account = 'david-rene@earth-engine-384112.iam.gserviceaccount.com'

# Enter the path to your credentials:
credsPath = '/dbfs/Filestore/tables/credentials.json'
# In our case, using a key that we uploaded through Databricks file upload:
credsPath = '/dbfs/FileStore/tables/earth_engine_384112_03e2e02ee924.json'

# We can then initialize a session:
credentials = ee.ServiceAccountCredentials(service_account, credsPath)
ee.Initialize(credentials)

# Let's test it out:
print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Using a private key uploaded to FSDH storage

# COMMAND ----------

import ee
import json

# Enter the email associated with your service account created in step 3:
service_account = 'my-service-account@...gserviceaccount.com'
# In our case:
service_account = 'david-rene@earth-engine-384112.iam.gserviceaccount.com'

# Enter the path to your credentials:
credsPath = '/mnt/fsdh-dbk-main-mount/path/to/credentials.json'
# In our case, using a key that we uploaded to FSDH storage:
credsPath = '/mnt/fsdh-dbk-main-mount/David/earth-engine-384112-72d27e31c3b7.json'

json_rows = spark.read.text(credsPath).collect() # Read the file using spark
creds = json.loads("".join([row.value for row in json_rows])) # Load it into a proper json/dict

# Dump into a json file with the original name but in filestore
newPath = "/dbfs/FileStore/tables/"+credsPath.split("/")[-1] 
with open(newPath, "w") as f: 
    json.dump(creds,f)

# We can then initialize a session:
credentials = ee.ServiceAccountCredentials(service_account, newPath)
ee.Initialize(credentials)

# Let's test it out:
print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())
