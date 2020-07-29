
Manage rq jobs with multiple or tree-like dependancy.

Create a "project" dictionary that contains an array of jobs.
```python
project = {'jobs':[
            {'func':simpleTask,'args': 1},
            {'func':simpleTask,'args': 2}]
            }
```
Then give it to the "manager" to complete it!

```python
q = Queue() 
managerJob = q.enque(manager,project)
projectResults = getProjectResults(managerJob)
```

## A few examples
Define a simple job:
```python
def simpleJob(x):
    return 2*x
```

### Run jobs in parallel:
Jobs in an array will be started immediately and run in parallel.
```Python
project = {'jobs':[
            {'func':simpleTask,'args': 1},
            {'func':simpleTask,'args': 2}]
            }
```
returns
```python
[2, 4]

```

### Run jobs in series:
If a job is marked as blocking, the following jobs will wait to run.
```Python
project = {'jobs':[
            {'func':simpleTask,'args': 1, 'blocking':True},
            {'func':simpleTask,'args': 2}]
            }
```
returns
```python
[2, 4]

```

### Run with dependent arguments:
A job can use the the results of a previous job as its inputs. It will wait for the previous job to finish, but it will not block later jobs.
```Python
project = {'jobs':[
            {'func':simpleTask,'args': 1},
            {'func':simpleTask, 'previousJobArgs': True}, # this job will wait
            {'func':simpleTask,'args': 3}] # this job will NOT wait
            }
```
returns
```python
[2, 4, 6]

```

### Run jobs with multiple dependancy:
A job can have child jobs. The parent job is not finised until all of the child jobs are finished. 
```Python
project = {'jobs':[
            {
                'blocking':True, # this job, and its child jobs, must finished before moving on.
                'jobs':[ 
                    {'func':simpleTask,'args': 1},
                    {'func':simpleTask,'args': 2}],
            },
            { # this job will only run when the blocking job above finishes.
                'func':simpleTask,'args': 3
            }
        ]}
```
returns
```python
[[2, 4], 6]

```

### Add jobs as you go
Define a job that creates an array of new jobs.
```Python
def addJobs(n):
    newJobArray = []
    for i in range(n):
        newJobArray.append({'func':simpleTask,'args': i})

    return {'result':2*n, 'addJobs':newJobArray}
```
Jobs will be appended to the current job array
```Python
project = {'jobs':[
            {
                'blocking':True, 
                'jobs':[ # these two jobs will be run first
                    {'func':simpleTask,'args': 1},
                    {'func':addJobs,'args': 2} # This job adds new jobs
                    # New Jobs are placed here
                    ], 
            },
            {'func':simpleTask,'args': 3}]
        }
```
returns
```python
[[2, 4, 8, 10], 6]

```

### Add job with child jobs as you go
Define a job that creates new a job filled with child jobs.
```Python
def addSubJob(n):
    newJobArray = []
    for i in range(n):
        newJobArray.append({'func':simpleTask,'args': i})

    newSubJob = {'jobs':newJobArray }
    return {'result':2*n, 'addJobs':newSubJob}
```
A sub job will be added with child jobs.
```Python
project = {'jobs':[
            {
                'blocking':True, 
                'jobs':[ # these two jobs will be run first
                    {'func':simpleTask,'args': 1},
                    {'func':addSubJob,'args': 2} # This job adds a new job with child jobs
                    # {'jobs': New child jobs are placed here}
                    ], 
            },
            {'func':simpleTask,'args': 2}]
        }
```
returns
```python
[[2, 4, [8, 10]], 6]

```

## Redis Help
Install Redis Server
```
sudo apt update
sudo apt install redis-server
```

Start Redis Server
```
redis-server
```

Run supervisor
```
supervisord
```

Clear Jobs / Clear Redis Cache (optional)
```
redis-cli FLUSHALL
```
