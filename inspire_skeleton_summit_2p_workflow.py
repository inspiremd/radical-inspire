import os
from radical.entk import Pipeline, Stage, Task, AppManager

# -----------------------------------------------------------------------------
# Set default verbosity and env variables for RabbitMQ

if os.environ.get('RADICAL_ENTK_VERBOSE') is None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = os.environ.get('RMQ_PORT', 5672)


# -----------------------------------------------------------------------------
def describe_MD_pipline():
    p = Pipeline()
    p.name = 'MD'

    # Docking rescroring stage
    s1 = Stage()
    s1.name = 'rescoring'

    # Docking rescroring task
    t1 = Task()
    t1.executable = ['/gpfs/alpine/scratch/mturilli1/bip179/bin/mmgbsa_wrapper.sh']

    # Alternative approach for later optimization
    # t2.pre_exec = t2_senv
    # t2.executable = ['python']
    # t2.arguments = ['1_mmgbsa.py', '-p', '"test"', '-n', '0']

    # Add the docking rescroring task to the docking rescroring stage
    s1.add_tasks(t1)

    # Add the docking rescroring stage to the pipeline
    p.add_stages(s1)

    return p


# -----------------------------------------------------------------------------
def describe_ML_pipline():
    p = Pipeline()
    p.name = 'ML'

    # Learning stage
    s1 = Stage()
    s1.name = 'learning'

    # Docking rescroring task
    t1 = Task()
    t1.executable = ['/gpfs/alpine/scratch/mturilli1/bip179/bin/run_learner_wrapper.sh']

    # Add the docking rescroring task to the docking rescroring stage
    s1.add_tasks(t1)

    # Add the docking rescroring stage to the pipeline
    p.add_stages(s1)

    return p


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # Project scratch directory
    pdir = '/gpfs/alpine/scratch/mturilli1/bip179/'

    # Execution environemt for task t2 1_mmgbsa.py
    # t2_senv = ['source %s/bin/setup.sh' % pdir]

    # Create a dictionary to describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {'resource': 'ornl.summit_prte',
                'queue'   : 'batch',
                'schema'  : '',
                'project' : 'bip179',
                'queue'   : 'batch',
                'walltime': 15,
                'cpus'    : 336,
                'gpus'    : 12}

    # Create Application Manager
    appman = AppManager(hostname=hostname, port=int(port))

    try:
        appman.resource_desc = res_dict

        p_md = describe_MD_pipline()
        p_ml = describe_ML_pipline()

        # Assign the workflow as a list of Pipelines to the Application Manager. In
        # this way, all the pipelines in the list will execute concurrently.
        appman.workflow = [p_md, p_ml]

        # Run the Application Manager
        appman.run()

    finally:
        appman.terminate()
