

def simpleTask(x):
    return 2*x


def addJobs(x):
    newJobs = []
    for i in range(x):
        newJobs.append({'func':simpleTask,'args': i})

    return {'result':2*x, 'addJobs':newJobs}


def addSubJob(x):
    newJobs = []
    for i in range(x):
        newJobs.append({'func':simpleTask,'args': i})

    return {'result':2*x, 'addJobs':{'jobs':newJobs }}