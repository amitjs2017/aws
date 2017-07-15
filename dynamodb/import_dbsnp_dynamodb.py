# This script tests the autoscaling feature of DynamoDB (introduced Jun 2017)
# Create a new table with the default read throughput of 5 read capacity units
# Run this script and monitor "Write Capacity" and "Throttled Write Requests" in CloudWatch for this table
# `batch_writer` in boto3 will automatically handle backing off and re-trying writes that failed because write throughput was exceeded
# DynamoDB autoscaling will periodically increase read capacity to keep up with the reads coming in
# When the script is done, 

import argparse
import logging
import sys

import boto3
from tqdm import tqdm

REGION = "us-east-1"


# ----------
# Setup logging
# ----------
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


def import_file(in_file, source):

	# FORMAT of input VCF file:
	# CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
	# 1	10583	rs58108140	G	A	.	.	RS=58108140;RSPOS=10583;dbSNPBuildID=129;SSR=0;SAO=0;VP=0x050000020001100016000100;WGT=1;VC=SNV;R5;KGPhase1;KGPROD;OTHERKG;CAF=[0.8558,0.1442];COMMON=1
	# 1	10611	rs189107123	C	G	.	.	RS=189107123;RSPOS=10611;dbSNPBuildID=135;SSR=0;SAO=0;VP=0x050000020001100014000100;WGT=1;VC=SNV;R5;KGPhase1;KGPROD;CAF=[0.9812,0.01882];COMMON=1
	# 1	13302	rs180734498	C	T	.	.	RS=180734498;RSPOS=13302;dbSNPBuildID=135;SSR=0;SAO=0;VP=0x050000000001100014000100;WGT=1;VC=SNV;KGPhase1;KGPROD;CAF=[0.8857,0.1143];COMMON=1
	# ...

	ddb = boto3.resource("dynamodb", region_name=REGION)
	table = ddb.Table(source)

	counter = 0

	with table.batch_writer() as batch:
		with open(in_file) as fh:
			for line in tqdm(fh):
				if line.startswith("#") or line.startswith("MT"):
					continue

				fields = line.split("\t")
				variant_id = fields[2]
				chrom = fields[0]
				start = int(fields[1]) - 1
				stop = int(fields[1])


				item = {}
				item["id"] = variant_id
				item["chr"] = chrom
				item["start"] = start
				item["stop"] = stop
				item["source"] = source

				batch.put_item(Item=item)

				counter += 1

	return counter


def main():

	# Get input file
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="The tab-delimited text file to import")
	parser.add_argument("source", help="Source abbreviation - used for table name & source column")
	args = parser.parse_args()
	in_file = args.file
	source = args.source

	logger.info("Importing data into DynamoDB")
	counter = import_file(in_file, source)
	logger.info("Finished importing {} dbSNP items into DynamoDB".format(counter))


if __name__ == "__main__":
	main()
