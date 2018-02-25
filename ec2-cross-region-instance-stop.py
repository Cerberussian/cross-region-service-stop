import boto3
import logging
from time import sleep, time

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the first connection
ec2_client = boto3.client('ec2')

#get regions
response = ec2_client.describe_regions()

#make a list of regions to loop through
region_list = [region['RegionName'] for region in response['Regions']]

################################# Services Functions #################################

#EC2
def stop_ec2_instances(region):
	client = boto3.client('ec2', region_name=region)
	response = client.describe_instances()

	for reservation in response['Reservations']:
		for instance in reservation['Instances']:
			logging.info('stopping: ' + instance['InstanceId'])

			try:
				client.stop_instances(
					InstanceIds=[instance['InstanceId']],
					Force=True,
					)
			except:
				logging.info('Instance cant be stopped at this moment')

#ASG
def set_asg_to_zero(region):
	client = boto3.client('autoscaling', region_name=region)
	logging.info('Getting list of ASGs')
	response = client.describe_auto_scaling_groups()

	if response['AutoScalingGroups']:
		logging.info('Found ASGs in ' + region + '. looping through ASGs to change desired to 0')
		for ASG in response['AutoScalingGroups']:
			logging.info('Changing min and desired of ' + ASG['AutoScalingGroupName'] + ' ASG in region ' + region + ' to 0')
			client.update_auto_scaling_group(
				AutoScalingGroupName=ASG['AutoScalingGroupName'],
				MinSize=0,
				DesiredCapacity=0
				)
	else:
		logging.info('No ASGs in ' + region)

#RDS
def terminate_rds_instances(region):
	client = boto3.client('rds', region_name=region)
	logging.info('Getting list of RDS instances')
	response = client.describe_db_instances()

	if response['DBInstances']:
		for db in response['DBInstances']:
			logging.info('Terminating ' + db['DBInstanceIdentifier'])
			try:
				client.delete_db_instance(
				DBInstanceIdentifier=db['DBInstanceIdentifier'],
				SkipFinalSnapshot=False,
				FinalDBSnapshotIdentifier=db['DBInstanceIdentifier'] + '-' + str(int(time()))
				)
			except:
				logging.info('There was a problem deleting RDS instance (check boto3 delete_db_instance documentation for possible reasons)')
	else:
		logging.info('No RDS instances in ' + region)

################################# Main Function #################################

def lambda_handler(event, context):

	#loop through regions and stop services
	for region in region_list:

		logging.info('Going through region ' + region)

		#EC2
		stop_ec2_instances(region)
		
		#ASG
		set_asg_to_zero(region)
		
		#RDS
		terminate_rds_instances(region)