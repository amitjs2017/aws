# EMR vs. AWS Batch

| [EMR](https://aws.amazon.com/emr/) | [Batch](https://aws.amazon.com/batch/) |
|---|---|
| Data-oriented | Process-oriented |
| Massively parallel "big data" processing: `Data lake ==> Parallel processing in cluster ==> Output data` | Executes jobs on machines without manual intervention where jobs can depend on other jobs or availability of input (sequencing & scheduling matters) |
| EMR supports Spark which can handle batch processing, stream processing, interactive queries, etc. | Handles only batch jobs; does not support streaming or interactive processing |
| Works best for a single large job processing a lot of data | Works best for multiple independent batch jobs. Batch can also call EMR as needed. |
| Underlying cluster must be setup before jobs can be submitted. Not as flexible as Batch in terms of changing cluster size & instance type after cluster setup. Cluster must be terminated manually or can be set up to terminate automatically after job completes. | Underlying cluster is managed by Batch. For managed clusters, Batch determines the instance type, cluster size, etc. automatically depending on workload and terminates instances when job queues are empty |
| Jobs run directly on cluster instances and are restricted to the Amazon Linux OS & languages supported by Spark (for Spark jobs) | Jobs run inside Docker containers on the cluster instances and can support any language/OS supported by Linux Docker environment |

## Ref: 
* AWS docs
* AWS Support
