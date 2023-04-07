## Overview  
Generate summary information for the distribution of giving data. This script is wrote in Python 3, and build with bazel (https://bazel.build).
It is implemented with default Python libraries, not third-party libraries are required.    

## Getting started  
### Build the script:   
1. install bazel   
2. run "make build"  
3. the built script is at 'bazel-bin/summerizer'   

### Example usages:  
- calculate the min, max, mean of the count of event_type per device_id:  
$> bazel-bin/summerizer ./data-dump --eval_type "device_id" --metrics "min,max,mean"  

- calculate the distribution of 'Squirrel' events:  
$> bazel-bin/summerizer ./data-dump --eval_key "Squirrel" --eval_type "event_type" --metrics "hist10"  

- specify the output directory:   
$> bazel-bin/summerizer ./data-dump --eval_key "Squirrel" --eval_type "event_type" --metrics "hist10" --output_dir /tmp  

### Example of the input data:  
A data folder contains data files. Only file has name pattern "ev_dump_*.csv" will be consumed.  
Assume the .csv data file has header.    
Example line of the file:  
"1595275375.814,0c428083,squirrel,e3d387ad18f528237bb7"

### Examples of output:  
A JSON object records the distribution value. Example output:  
{
    "D5408274": {"cnt": 4, "mean": 310.75, "max": 828, "min": 109}, 
    "9621EBC2": {"cnt": 4, "mean": 1458.25, "max": 5535, "min": 26},
    ...
}  
  
{"SQUIRREL": {"cnt": 10, "hist10": {"820": 1, "5530": 1, "1400": 1, "4920": 1, "720": 1, "150": 1, "410": 1, "580": 1, "130": 1, "140": 1}}}  

## Dev guide   
The data processing logic of this scripts is:  
1. count data files one by one.  
2. for each data file, count the (device_id, event_type) pairs. Update the results to a central key-value storage. A fake version by using the Python dict object is implemented in this script.  
3. Once we have the counting results. The statistics will be calculated in one-pass.  

To develop more metrics:  
1. if the metric can be calculated in one-pass, follow the code in 'summ/metrics.py'
2. if a complex metric need to be calculated, we can write new functions to process the data in the key-value storage.

To improve scalability:
1. if the number of unique (device_id, event_type) is high, the default Python dict will not work. We can either use an external Key-value DB or do an key partition by improving the implementation of KVStore class in 'summ/kv_store.py'.
2. if there are many files in the data folder, we can use cache the file names to task Queue like celery, and create multiple workers with the "update_by_file()" function in "summ/counter.py"










