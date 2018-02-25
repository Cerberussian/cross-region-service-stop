# cross-region-service-stop

No more facepalms if you forget to stop resources in AWS!

No more sweating while staring at your unexpected AWS bills!

No more exhausting your free trail!  

This lambda can save you some $$$!

This lambda will run at scheduled time and take care of stopping your resources!

Designed specially for AWS sandboxes.

------

You should put this lambda just in one region

You can install python tool to test lambda locally:
https://github.com/Cerberussian/python-lambda-local

After that, you can use this command to try lambda locally:

python-lambda-local -f lambda_handler ec2-cross-region-instance-stop.py scheduled-event.json -t 120

If you have any questions, feel free to contact me

------
# Update - 25/02/18


* Added checks for auto scaling groups - setting its minimum and desired to 0 if found

* Added checks for RDS - taking final snapshot and terminating instances.
Deletion could fail due to different reasons described in official documentation: http://boto3.readthedocs.io/en/latest/reference/services/rds.html#RDS.Client.delete_db_instance

* Restructured lambda and now its more decoupled. This also allows you now to easily disable services you dont want to terminate / stop by commenting out relevant function call in main

* Added permissions needed for lambda to run. Lambda got extensive list permissions but limited write permissions

* Changed name of repo from ec2-cross-region-instance-stop to cross-region-service-stop
