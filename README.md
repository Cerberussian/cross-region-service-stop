# ec2-cross-region-instance-stop

You should put this lambda just in one region

You can install python tool to test lambda locally:
https://github.com/Cerberussian/python-lambda-local

After that, you can use this command to try lambda locally:

python-lambda-local -f lambda_handler ec2-cross-region-instance-stop.py scheduled-event.json -t 120


# Update

* Added checks for auto scaling groups - setting its minimum and desired to 0 if found

* Added checks for RDS - taking final snapshot and terminating instances.
Deletion could fail due to different reasons described in official documentation: http://boto3.readthedocs.io/en/latest/reference/services/rds.html#RDS.Client.delete_db_instance

* Restructured lambda and now its more decoupled. This also allows you now to easily disable services you dont want to terminate / stop by commenting out relevant function call in main

* Added permissions needed for lambda to run. Lambda got extensive list permissions but limited write permissions
