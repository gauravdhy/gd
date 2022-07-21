import json
#from botocore.vendored import requests
import requests
import gzip
import base64
import os 
import logging 

#Step 1: Run the API page that will generate the cloudwatch logs for the API-GW. 
#        API-GW generated cloudwatch logs. Cloudwatch logs subscribe to this Lambda function 
#        This Lambda function gets auto-trigerred
#Step 2: Read the API-GW logs into a variable cw_data. These logs are base64 encoded and zipped.    
#Step 3: compressed_payload=decode cw_data
#Step 4: uncompressed_payload=unzip the decoded cw_data
#Step 5: payload = Deseralize the data from Step-4 using json.loads (output is a list)
#Step 6: We are going to read the data associated with the key logEvents
#Step 7: We will loop through this data and concatenate it into a string
#Step 8: We will send a POST request to our Webserver that is running a webserver on port 8080. The concatenated_log is the body



#Read the cloudwatch log in Lambda
def lambda_handler(event, context):
    
    # Read the API Logs
    cw_data = event['awslogs']['data']
    
    #Decode cw_data
    compressed_payload = base64.b64decode(cw_data)
    
    #Uncompress 
    uncompressed_payload = gzip.decompress(compressed_payload)
    
    #Deserialize the uncompressed payload in a list
    payload = json.loads(uncompressed_payload)

    #Let's dump the output in the logs
    #print(f"Payload is: {payload}")
    
    #Let's look for all the data in the payload['logEvents'] 
    log_events = payload['logEvents']
    concatenated_log=[]
    
    ###print(f"{log_events}")
    for log_event in log_events:
            #Let's concatenate each into a log_event into concatenated_log
            concatenated_log.append(log_event)
        
    #Let's print the concatenated_log file in the log for this Lambda function
    print("Finished creating concatenated_log")
    #print(f"Concatenated log file is: {concatenated_log}")
        

#Time to connect to our webserver    
    #This is our webserver internal IP
    url="http://ip-172-31-25-36.ec2.internal:8080"
    print(f"Connecting to webserver {url}")
        
    #Let's send in the post request the concatenated logs as the body as a string
    response=requests.post(url,json.dumps(concatenated_log))
    
    #Let's check the response from the webserver
    print(f"This is what the webserver returned: {response.text}")
    
    #Let's return status: 200 and concatenated_logs to our terminal here as well
    return {
       'statusCode': 200,
        'body': json.dumps(concatenated_log)
    }
