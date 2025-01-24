AutomaticUpdatesIntoFeatureService
==================================

## ! REPO ARCHIVED !
This repo has not been reviewed nor updated in many years. Archiving it in case it's contents are still useful, but recommend looking to [ArcGIS Pro doc](https://pro.arcgis.com/en/pro-app/latest/help/main/welcome-to-the-arcgis-pro-app-help.htm), [ArcGIS Enterprise doc](https://enterprise.arcgis.com/en/documentation/) and [esri blogs](https://www.esri.com/arcgis-blog/) for up to date best practices.

----

The Python script grabs a point location from an external site that is constantly updating. It then pulls the feature information out, constructs a JSON object and submits an updated point to an ArcGIS.com hosted feature service. A feature service with a matching schema must already exist for this script to work correctly.

See more information on the [associated ArcGIS Blog post](http://blogs.esri.com/esri/arcgis/2014/10/07/using-python-to-push-updates-to-a-hosted-feature-service-from-an-external-source/).

## Instructions

1. Download the **UpdatePointFromExternalAPI.py** (Hint: Click the `Download ZIP` button on the right)
2. Save the files to a local directory
3. Setup a feature service with your ArcGIS.com account. The instructions [on this blog post](http://blogs.esri.com/esri/arcgis/2014/09/22/how-to-create-a-hosted-feature-service/) explain different ways to create the service. The required feature service for this example is simple; the first option of creating a service from ArcGIS Online would suffice. 
  1. From **My Content**, click **Create Layer**.
  2. Select **from a URL to a feature layer**
  3. Enter:  http://services1.arcgis.com/hLJbHVT9ZrDIzK0I/arcgis/rest/services/issSchema/FeatureServer/0
  4. Select **next**, accept the default extent and enter some useful **tags** and **summary** information on the final page. Remember the **title**, you'll need to enter this information into the Python script.
  5. Click **done**.
  6. Set sharing options for the service. You **do not** need to enable editing.
4. Edit the Python script you saved previously and update the variables at the top of the script. 
  1. A *username* and *password* that owns the service
  2. The *serviceName*, set previously
  3. The full URL to the feature service you just created
  4. The URL of the service to get updates from (Note - simply replacing this URL with one of your choice will probably require further script updates. See the next section for details)
  5. How long to *pauseTime* before updating.
5. Run the script. As-is, it'll update the point every 5 minutes. Modify this value to your needs.

## Making it Update for you
Different parts of the script need to be updated to make it work with your external content. 

1. Around line 180, a *req* -uest is made to get updated information from an external source. The response comes back and is loaded into a json object ( *issPoint* ). Depending on the API you're consuming, you may or may not have to modify this part.
2. You'll almost certainly have to update the *Y*, *X*, and *ptTime* variables. The code here is specific to grabbing values out of this specific json structure. You may need to grab more information, or append this information to existing features. However you change the code, make sure you appropriately update the *updatePoint* function (148) and where the function is called from (194).
3. The second bit of code to update will be the *jsonPoint* function inside the class (around line 66). This function is set to return a simple point object with a schema that matches the feature service being updated. Update this code with the modifications made previously so the features will update your hosted feature service layer.  
4. You may need to update the *fillEmptyGeo* function as well. If your hosted service is empty the first time you run the script, you'll need to update this function. The entire script works by "updating" existing features. This means you need one or more values to already exist in the service.
5. The script has been hard coded to always update a layer with the index of "0". If the layer you're updating is not the first layer in the service (0), or you have multiple layers to update, you'll need to modify the references throughout the script.

## Resources

* [ArcGIS REST API Update Features](http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Update_Features/02r3000000zt000000)


## Licensing
Copyright 2014 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's [license.txt]( https://github.com/update-hosted-feature-service/master/license.txt) file.

[](Esri Tags: ArcGIS.com Online Update Hosted Feature Services Automate Python Publish)
[](Esri Language: Python)​
