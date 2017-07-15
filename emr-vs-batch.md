# EMR vs. AWS Batch

## [EMR](https://aws.amazon.com/emr/)
* Data-specific
* Massively parallel "big data" processing: Data lake ==> Parallel processing in cluster ==> Output data
* EMR support Spark and handles batch processing, streaming, interactive queries, etc.
* Works best for a single large job processing a lot of data
* Underlying cluster must be setup before jobs can be submitted. Not as flexible as Batch in terms of changing cluster size & instance type.
* Jobs run directly on EMR instances and are restricted to Amazon Linux & languages supported by Spark (for Spark jobs)


## [Batch](https://aws.amazon.com/batch/)
* Process-specific
* Executes jobs on 1 or more machines without manualy intervention where jobs can depend on other jobs or availability of input
* Does not support interactive processing
* Works best for multiple independent batch jobs. Batch can also call EMR as needed.
* Underlying cluster is managed by Batch. For managed clusters, Batch determines the instance type, cluster size, etc. depending on workload and terminates instances when job queues are empty
* Jobs run inside Docker container and can support any language/framework supported by Linux Docker environment

## Ref: 
* AWS docs
* AWS Support
