from rq import Queue
from redis import Redis

from rq_manager import manager, getProjectResults

from exampleTasks import addSubJob, simpleTask, addJobs, addSubJob

#### Examples are slow because "sleepTime" default is 1 second  ####

# Tell RQ what Redis connection to use
q = Queue(connection=Redis())

### Run jobs in parallel:
project = {'jobs':[
            {'func':simpleTask,'args': 1},
            {'func':simpleTask,'args': 2}]
            }

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
print(projectResults)

### Run jobs in series:
project = {'jobs':[
            {'func':simpleTask,'args': 1, 'blocking':True},
            {'func':simpleTask,'args': 2}]
            }

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
print(projectResults)

### Run with dependent arguments:
project = {'jobs':[
            {'func':simpleTask,'args': 1},
            {'func':simpleTask, 'previousJobArgs': True}, # this job will wait
            {'func':simpleTask,'args': 3}] # this job will NOT wait
            }

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
print(projectResults)

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
print(projectResults)

### Add jobs as you go
project = {'jobs':[
            {
                'blocking':True, 
                'jobs':[ # these two jobs will be run first
                    {'func':simpleTask,'args': 1},
                    {'func':addJobs,'args': 2} # This job adds new jobs
                    # New jobs are placed here
                    ], 
            },
            {'func':simpleTask,'args': 3}]
        }

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
print(projectResults)

### Add a job with child jobs as you go
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

managerJob = q.enqueue(manager,project)
projectResults = getProjectResults(managerJob)
print(projectResults)