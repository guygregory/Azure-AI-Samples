import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.resource import ResourceManagementClient
import webbrowser
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Get the Azure subscription ID from the .env file
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

# Authenticate with Azure
credential = DefaultAzureCredential()

# Create a Cognitive Services Management client
client = CognitiveServicesManagementClient(credential, subscription_id)

# Initialize the Resource Management client
resource_client = ResourceManagementClient(credential, subscription_id)

# Initialize an empty DataFrame with the specified columns
deployment_df = pd.DataFrame(columns=["Resource Group", "OpenAI Service Name", "Deployment Name", "Model Name", "Version"])

# Filter for OpenAI instances and list model deployments
for resource_group in resource_client.resource_groups.list():
    accounts = client.accounts.list_by_resource_group(resource_group.name)  # Corrected line
    for account in accounts:
        if account.kind == 'OpenAI':
            # Correctly access deployment properties using dot notation
            deployments = client.deployments.list(resource_group.name, account.name)
            deployment_info = [{"deploymentname": deployment.name, "modelname": deployment.properties.model.name, "version": deployment.properties.model.version} for deployment in deployments]
            
            # output deployment_info in a more readable format
            for deployment in deployment_info:
                #print(f"Deployment Name: {deployment['deploymentname']}, Model Name: {deployment['modelname']}, Version: {deployment['version']}")
                # Inside the loop where you add rows to the DataFrame
                new_row = pd.DataFrame([{
                    "Resource Group": resource_group.name,
                    "OpenAI Service Name": account.name,
                    "Deployment Name": deployment['deploymentname'],
                    "Model Name": deployment['modelname'],
                    "Version": deployment['version']
                }])
                
                deployment_df = pd.concat([deployment_df, new_row], ignore_index=True)

# Optionally, display the DataFrame
#print(deployment_df)

# Convert the DataFrame to HTML
html_string = deployment_df.to_html()

# Define the path for the HTML file (e.g., in the current working directory)
html_file_path = os.path.join(os.getcwd(), "deployments.html")

# Write the HTML string to the file
with open(html_file_path, 'w') as f:
    f.write(html_string)

# Open the HTML file in the default browser
webbrowser.open('file://' + html_file_path)