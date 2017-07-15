# ABOUT:
# Create & upload zip file containing Python 3.6 Lambda function code to S3 
# Update function code for Lambda function

# ASSUMPTIONS: 
# EC2 instance on which this scripts runs is associated with an IAM role with appropriate permissions to access S3 & Lambda
#
# This script must be run from virtualenv dir
# Expected directory structure:
# - script1.py
# - script2.py
# - lib/
#   |
#   - python3.6/
#     |
#     site-packages/


BASE_DIR=/home/ec2-user/<DIR>
ZIP_FILE=lambda_function.zip

REGION=<region>
S3_BUCKET=<s3_bucket>
LAMBDA_FUNCTION_NAME=<function_name>


echo "Zipping files to $BASEDIR/$ZIP_FILE"
cd $BASE_DIR
rm -rf $ZIP_FILE
zip $BASE_DIR/$ZIP_FILE *.py

cd $BASE_DIR/lib/python3.6/site-packages/
zip -qr $BASE_DIR/$ZIP_FILE .


echo "Uploading $ZIP_FILE to S3"
aws s3 cp $BASE_DIR/$ZIP_FILE s3://$S3_BUCKET/


echo "Updating Lambda function code"
aws lambda update-function-code --region $REGION --function-name $LAMBDA_FUNCTION_NAME --s3-bucket $S3_BUCKET --s3-key $ZIP_FILE

echo "Done"
