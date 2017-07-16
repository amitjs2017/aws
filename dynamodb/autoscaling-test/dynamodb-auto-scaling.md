### DynamoDB Auto Scaling

* Can handle occasional spikes in throughput with built-in burst capacity
* For sustained increases in reads/writes, can increase capacity as often as necessary to keep up with incoming reads/writes
* `Scale up` occurs when total consumed capacity for 5 1-min evaluation periods > threshold set for the 5 min period
* Can decrease capacity up to 4 times a day (where day is defined according to GMT time zone). Additionally, if there is no decrease in the past 4 hours, then additional decrease is allowed. So total number of decreases allowed is 9 (4 in the first 4 hours + 1 in each of the next five 4-hr blocks).
* `Scale down` follows same method as scale UP but uses 15 min evaluation period instead of 5 mins (i.e., scale up aggresively and scale down slowly)
* Only consumed capacity metrics are used to determine auto scaling

### Ref: 
* AWS Docs
* AWS Support
