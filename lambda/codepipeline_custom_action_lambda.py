# Example of a Lambda function that can be called from a custom action in AWS CodePipeline

from base64 import b64decode
import boto3
import json
import logging
import os
import os.path
import requests
import sys


def setup_logging():
    logger = logging.getLogger()

    # remove settings made by AWS Lambda
    for h in logger.handlers:
      logger.removeHandler(h)

    h = logging.StreamHandler(sys.stdout)

    FORMAT = '%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s %(message)s'
    h.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

    return logger

logger = setup_logging()


def codepipeline_failure(job_id, msg):

    logger.info("Sending job failure result to CodePipeline")

    if msg is None:
        raise Exception("No error message specified!")

    logger.error(msg)

    try:
        codepipeline = boto3.client("codepipeline")
        codepipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                "type": "JobFailed",
                "message": msg
            }
        )
        logger.info("Finishing sending job failure result to CodePipeline")
        return False
        
    except Exception as e:
        raise Exception("Failed to send failure result to codepipeline: " + str(e))


def codepipeline_success(job_id):

    logger.info("Sending job success result to CodePipeline")

    try:
        codepipeline = boto3.client("codepipeline")
        codepipeline.put_job_success_result(jobId=job_id)
        logger.info("Finished sending job success result to CodePipeline")
        return True
        
    except Exception as e:
        codepipeline_failure(job_id, "Failed to send success result to codepipeline: " + str(e))


def get_job_id(event):
    
    try:
        logger.info("Getting job id for CodePipeline custom action")
        job_id = event["CodePipeline.job"]["id"]
        logger.info("Got " + job_id)

    except KeyError as e:
        logger.error("Cannot find job id for CodePipeline custom action using key event['CodePipeline.job']['id']: " + str(e))
        raise

    return job_id


def construct_notification(msg):

    logger.info("Constructing Slack notification")

    slack_message = {}
    slack_message["channel"] = 'devops'
    slack_message["text"] = msg

    logger.info("Returning: " + slack_message)

    return slack_message


def notify_slack(job_id, slack_message):
    
    ENCRYPTED_SLACK_URL = os.environ["ENCRYPTED_SLACK_URL"]
    SLACK_URL = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_SLACK_URL))['Plaintext']
    SLACK_URL = "https://" + SLACK_URL.decode("utf-8")

    try:
        response = requests.post(SLACK_URL, json.dumps(slack_message), headers={"Content-Type": "application/json"})
        logger.info("Message posted to channel " + slack_message['channel'])

    except Exception as e:
        codepipeline_failure(job_id, "POST request to Slack failed: " + str(e))
        raise 


def main(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))

    # Get job id for CodePipeline custom action
    job_id = get_job_id(event)


    # Point dev alias to latest version
    slack_message = construct_notification("CodePipeline custom action: Hello from Lambda!")
    notify_slack(job_id, slack_message)


    # Notify CodePipeline
    codepipeline_success(job_id)

