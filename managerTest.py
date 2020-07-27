
from rq import Queue
from redis import Redis

from manager import manager, waitForProjectResults
import tasks

import json
from pprint import pprint

def jsonCopy(d):
    return json.loads(json.dumps(d))

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn,is_async=True)  # no args implies the default queue


jobA_args = {
    'description':'jobA',
    'n_newJobs':2,
}

jobB_args = {
    'description':'jobB',
    'n_newJobs':3,
}

someJobs = []
durrations = range(3)
for durration in durrations:
    jobA_args['durration'] = durration+1
    jobB_args['durration'] = durration+1

    someJobs.append({
        'jobs':[{
                'jobs':[{
                    'func':tasks.makeMoreJobs,
                    'args': jsonCopy(jobA_args)
                    }]
                },
                {
                'jobs':[{
                    'func':tasks.makeMoreJobs,
                    'args': jsonCopy(jobB_args)
                    },]
                }]
            })


project = {
        'jobs':[
            {
            'jobs':someJobs
            },
            {
            'func':tasks.jobReport,
            'previousJobArgs': True,
            }
    ]}


managerJob = q.enqueue(manager,project)

projectResults = waitForProjectResults(managerJob)
pprint(projectResults[-1])

