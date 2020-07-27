
## rq-manager
Manage jobs with multiple or tree-like dependancy.

Create a "project", which is a tree of jobs, then give it to the "manager" to complete it!

managedProject = q.enque(manager,project)

## A few trivial examples.
Define a simple job:
```python
def simpleJob(x):
    return 2*x
```

### Run jobs in parallel
Jobs in an array will be started immediately and run in parallel.
```Python
project = {'jobs':[
            {'func':simpleTask,'args': 1},
            {'func':simpleTask,'args': 2}]
            }
```

### Run jobs in series:
If a job is marked as blocking, the following jobs will wait to run.
```Python
project = {'jobs':[
            {'func':simpleTask,'args': 1, 'blocking':True},
            {'func':simpleTask,'args': 2}]
            }
```

### Run with dependent arguments:
A job can use the the results of a previous job as its inputs. It will wait for the previous job to finish, but it will not block later jobs.
```Python
project = {'jobs':[
            {'func':simpleTask,'args': 1},
            {'func':simpleTask, 'previousJobArgs': True}, # this job will wait to start until the previous job is finished
            {'func':simpleTask,'args': 3}] # this job will NOT wait
            }
```

### Run jobs with multiple dependancy:
A job can have child jobs. The parent job is not finised until all of the child jobs are finished. 
```Python
project = {'jobs':[
            {
                'blocking':True # this job, and its child jobs, must finished before moving on.
                'jobs':[ 
                    {'func':simpleJob,'args': 1},
                    {'func':simpleJob,'args': 2}],
            },
            { # this job will only run when the blocking job above finishes.
                'func':simpleJob,'args': 2}]
            }
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
                    {'func':simpleTask,'args': 2},
                    {'func':addJobs,'args': 4} # This job adds new jobs
                    # New Jobs are placed here
                    ], 
            },
            {'func':simpleTask,'args': 2}]
        }
```

### Add sub jobs as you go
Define a job that creates new subjob filled with jobs.
```Python
def addSubJob(n):
    newJobArray = []
    for i in range(n):
        newJobArray.append({'func':simpleTask,'args': i})

    newSubJob = {'jobs':newJobArray }
    return {'result':2*n, 'addJobs':newSubJob}
```
A new sub job with subjobs will 
```Python
project = {'jobs':[
            {
                'blocking':True, 
                'jobs':[ # these two jobs will be run first
                    {'func':simpleTask,'args': 2},
                    {'func':addSubJob,'args': 4} # This job adds a new job with subjobs
                    # {'jobs': New Jobs are placed here}
                    ], 
            },
            {'func':simpleTask,'args': 2}]
        }
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

Clear Redis Cashe (optional)
```
redis-cli FLUSHALL
```

Run supervisor
```
supervisord
```
