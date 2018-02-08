# ec2-cross-region-instance-stop

You should put this lambda just in one region

You can install python tool to test lambda locally:
https://github.com/Cerberussian/python-lambda-local

After that, you can use this command to try lambda locally:
python-lambda-local -f lambda_handler ec2-cross-region-instance-stop.py scheduled-event.json -t 120
