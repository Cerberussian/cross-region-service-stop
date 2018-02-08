import boto3
import logging
import time

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2_client = boto3.client('ec2')

#get regions
response = ec2_client.describe_regions()

#list regions
region_list = [region['RegionName'] for region in response['Regions']]

def lambda_handler(event, context):

    #go through regions and stop instances
    for region in region_list:

    	logging.info('Going through region ' + region)

    	ec2_client = boto3.client('ec2', region_name=region)

        #filter the instances
        response = ec2_client.describe_instances()

        for reservation in response['Reservations']:
        	for instance in reservation['Instances']:
        		logging.info('stopping: ' + instance['InstanceId'])
  				#instanceids accaptes only lists
        		listed_id = [instance['InstanceId']]

        		try:
        			ec2_client.stop_instances(InstanceIds=listed_id,Force=True)
        		except:
        			logging.info('Instance cant be stopped') 

        #for local testing
        #time.sleep(1)