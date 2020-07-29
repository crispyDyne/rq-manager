import time
import json

import numpy as np

def jsonCopy(d):
    return json.loads(json.dumps(d))

def makeMoreJobs(args):
    durration = args['durration'] * np.random.rand() # exact durration is not clear
    time.sleep(durration) # do some work

    # create new jobs
    latJobs = []
    latArgs = args
    for n in range(args['n_newJobs']):
        latArgs['jobNumber'] = n
        latJobs.append({'func':doAJob,'args': jsonCopy(latArgs)})

    # format output
    textResult = 'makeMoreJobs - ' + args['description'] +':' + str(args['durration']) + ' - durration: ' + str(durration)
    print(textResult) # just for debuging
    
    # The new project can be as simple or complicated as you would like. 
    newProject = {'jobs':latJobs }

    # this format is required in order to add jobs
    return {'result':textResult ,'addJobs':newProject} # {'result":anything, 'addJobs':{another project!}]

def doAJob(args):
    # do some work
    durration = args['durration'] * np.random.rand() # exact durration is not clear
    time.sleep(durration)

    # format output
    textResult = 'doAJob - ' + args['description'] + ' durration:' + str(durration) + ' jobNumber:' + str(args['jobNumber'])
    print(textResult)

    return textResult # for normal jobs, results can be whatever you want

def jobReport(args): 
    print('Job Report:')
    print(args)
    return args

