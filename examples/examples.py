from rq import Queue
from redis import Redis

from rq_manager import manager, getProjectResults
from exampleTasks import addSubJob, simpleTask, addJobs, addSubJob

import json
from pprint import pprint

def jsonCopy(d):
    return json.loads(json.dumps(d))

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn,is_async=True)  # no args implies the default queue

### Run jobs in parallel:
project = {'jobs':[
            {'func':simpleTask,'args': 1},
            {'func':simpleTask,'args': 2}]
            }

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
pprint(projectResults)

### Run jobs in series:
project = {'jobs':[
            {'func':simpleTask,'args': 1, 'blocking':True},
            {'func':simpleTask,'args': 2}]
            }

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
pprint(projectResults)

### Run with dependent arguments:
project = {'jobs':[
            {'func':simpleTask,'args': 1},
            {'func':simpleTask, 'previousJobArgs': True}, # this job will wait
            {'func':simpleTask,'args': 3}] # this job will NOT wait
            }

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
pprint(projectResults)

### Run jobs with multiple dependancy:
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

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
pprint(projectResults)

### Add jobs as you go
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

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
pprint(projectResults)

### Add a job with child jobs as you go
project = {'jobs':[
            {
                'blocking':True, 
                'jobs':[ # these two jobs will be run first
                    {'func':simpleTask,'args': 1},
                    {'func':addSubJob,'args': 2} # This job adds a new job with child jobs
                    # {'jobs': New Jobs are placed here}
                    ], 
            },
            {'func':simpleTask,'args': 2}]
        }

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
pprint(projectResults)