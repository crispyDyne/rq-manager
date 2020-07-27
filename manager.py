import collections
import time 
# from pprint import pprint

from rq import Queue
from redis import Redis

import json
def jsonCopy(d): # used to deep copy dictionaries 
    return json.loads(json.dumps(d))

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

def manager(project):

    jobsArefinished = runJobs(project['jobs'])   

    if jobsArefinished:
        project['status'] = 'finished'
    else:
        # Assign defaults if not set.
        if 'loop' not in project: project['loop'] = 0
        if 'maxLoop' not in project: project['maxLoop'] = 100
        if 'sleepTime' not in project: project['sleepTime'] = 0.5

        if (project['loop'] < project['maxLoop']):
            project['loop'] += 1 # keep track of the number of loops 
            time.sleep(project['sleepTime']) # wait before requeueing the project
            
            newProject = q.enqueue(manager,project) # requeue the project

            project['id']= newProject.id # record the new job id (allows tracking of project as it gets requeued)
            project['status'] = 'started'
        else:
            project['status'] = 'failed'

    return project


def runJobs(jobs):
    finished = True # are all jobs in the project finished? Requires all jobs and subjobs to be finished.
    for job_ind, job in enumerate(jobs):
        # If this job is already done, Move to the next job!
        if 'status' in job and (job['status'] == 'finished'): continue 

        if 'jobs' in job: # if the job has subjobs
            subJobsFinished = runJobs(job['jobs']) # delegate to another manager!
            finished = finished and subJobsFinished  # Project might be done. 
            if subJobsFinished:
                job['status'] = 'finished'

        elif 'func' in job: # if the job has has a function to evaluate
            # If the job has not started, get started! (jobs without status are waiting to start)
            if 'status' not in job:
                if job.get('previousJobArgs',False): # use the previous jobs results as arguments for this job
                    previousJob = jobs[job_ind-1]
                    if 'status' in previousJob and previousJob['status'] == 'finished': # make sure the previous job is finished
                        args = getJobResults(previousJob)
                    else: 
                        finished = False
                        continue 
                else: # or simply use the provided arguments
                    args = jsonCopy(job['args'])

                job_temp = q.enqueue(job['func'],args) # queue the job.
                job['id'] = job_temp.id # store the job id so we can keep track of its progress. 

                finished = False  # The jobs are not finished, we just started a job!
                job['status'] = 'started' # update job status

            # If the job has started, then check of its progress. 
            elif job['status'] == 'started':
                q_job = q.fetch_job(job['id'])
                status = q_job.get_status()

                if status == 'finished':
                    result = q_job.result
                    job['status'] = 'finished' # this job is finished
                    if isinstance(result,collections.Mapping) and 'addJobs' in result:
                        if isinstance(result['addJobs'],list):
                            jobs.extend(result['addJobs'])
                        else:
                            jobs.append(result['addJobs']) # Add new jobs to the project.
                        job['result'] = result['result'] # Save results of this job.
                        finished = False # The jobs are not finished, we just added more jobs!
                    else:
                        job['result'] = result
                else:
                    finished = False # This job does not have results, so the project is not finished

        # if the job is not finished, and blocking, we cannot move onto the next job. We break and wait...
        if not finished and job.get('blocking',False): 
                break
    
    return finished

def getJobResults(job): 
    # Get results of a job. If a job has subjobs, then an array of results will be returned.
    if 'func' in job:
        results = job['result']
    else:
        results = []
        for j in job['jobs']:
            results.append(getJobResults(j)) # recursive 

    return results

def waitForProjectResults(managerJob):
    project = None
    finished = False
    while not finished:
        time.sleep(.01)
        if managerJob.result:
            
            project = managerJob.result
            status = project['status']
            finished = status == 'finished' or status =='failed'

            if 'id' in project:
                managerJob = q.fetch_job(project['id'])

    return getJobResults(project)