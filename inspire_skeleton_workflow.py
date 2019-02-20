import os
from radical.entk import Pipeline, Stage, Task, AppManager

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') is None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

# Assumptions:
# - Each MD step runs for ~2h
# - Overheads+other workflow steps 0.5h
# - <= 300 concurrent tasks
# - Summit's scheduling policy [1]
#
# Resource rquest:
# - 46 <= nodes < 92 with 6h walltime.
#
# Workflow [2]:
# - 46 <= pipelines < 91
# - 2*45 <= Docking/MD stages < 2*90 (2 * (45 concurrent 2 hours-long stages)
#   limited by 6h walltime)
#
# The workflow has two types of pipelines: Head and MD. The Head Pipeline
# consists of 1 Stage with 2 Tasks: Generator and ML/AL. The MD Pipeline
# consists of 2 stages: the 1st stage has 1 Docking task; the 2nd stage has 6
# OpenMM tasks, each using 1 GPU.
#
# [1] https://www.olcf.ornl.gov/for-users/system-user-guides/summit/summit-
#     user-guide/#scheduling-policy
# [2] https://docs.google.com/drawings/d/1vxudWZtKrF6-
#     O_eGLuQkmzMC9T8HbEJCpYbRFZ3ipnw/


CUR_NEW_STAGE = 0
# MAX_NEW_STAGE = 90

# For local testing
MAX_NEW_STAGE = 3


def generate_MD_pipeline():

    def describe_MD_pipline():
        p = Pipeline()
        p.name = 'MD'

        # Docking stage
        s1 = Stage()
        s1.name = 'Docking'

        # Docking task
        t1 = Task()
        t1.executable = ['sleep']
        t1.arguments = ['30']

        # Add the Docking task to the Docking Stage
        s1.add_tasks(t1)

        # Add Docking stage to the pipeline
        p.add_stages(s1)

        # MD stage
        s2 = Stage()
        s2.name = 'Simulation'

        # Each Task() is an OpenMM executable that will run on a single GPU.
        # Set sleep time for local testing
        for i in range(6):
            t2 = Task()
            t2.executable = ['sleep']
            t2.arguments = ['60']

            # Add the MD task to the Docking Stage
            s2.add_tasks(t2)

        # Add post-exec to the Stage
        s2.post_exec = {
                            'condition': func_condition,
                            'on_true': func_on_true,
                            'on_false': func_on_false
                        }

        # Add MD stage to the MD Pipeline
        p.add_stages(s2)

        return p

    def func_condition():
        '''
        Adaptive condition

        Returns true ultil MAX_NEW_STAGE is reached. MAX_NEW_STAGE is
        calculated to be achievable within the available walltime.

        Note: walltime is known but runtime is assumed. MD pipelines might be
        truncated when walltime limit is reached and the whole workflow is
        terminated by the HPC machine.
        '''
        global CUR_NEW_STAGE, MAX_NEW_STAGE

        if CUR_NEW_STAGE <= MAX_NEW_STAGE:
            return True

        return False

    def func_on_true():

        global CUR_NEW_STAGE

        CUR_NEW_STAGE += 1

        describe_MD_pipline()

    def func_on_false():
        print 'Done'

    p = describe_MD_pipline()

    return p


def generate_ML_pipeline():

    # Create a Pipeline object
    p = Pipeline()
    p.name = 'ML'

    # Create a Stage object
    s1 = Stage()
    s1.name = 'Generator-ML'

    # the generator/ML Pipeline will consist of 1 Stage, 2 Tasks Task 1 :
    # Generator; Task 2: ConvNet/Active Learning Model
    # NOTE: Generator and ML/AL are alive across the whole workflow execution.
    # For local testing, sleep time is longer than the total execution time of
    # the MD pipelines.

    t1 = Task()
    t1.name = "generator"
    t1.pre_exec = []
    t1.pre_exec += ['module load python/2.7.15-anaconda2-5.3.0']
    t1.pre_exec += ['module load cuda/9.1.85'] 
    t1.pre_exec += ['module load gcc/6.4.0']
    t1.pre_exec += ['source activate snakes']
    t1.executable = ['python']
    t1.arguments = ['/ccs/home/jdakka/tf.py']
    s1.add_tasks(t1)

    t2 = Task()
    t2.name = "ml-al"
    t2.pre_exec = []
    t2.pre_exec += ['module load python/2.7.15-anaconda2-5.3.0']
    t2.pre_exec += ['module load cuda/9.1.85'] 
    t2.pre_exec += ['module load gcc/6.4.0']
    t2.pre_exec += ['source activate snakes']
    t2.executable = ['python']
    t2.arguments = ['/ccs/home/jdakka/tf.py']
    s1.add_tasks(t2)

    # Add Stage to the Pipeline
    p.add_stages(s1)

    return p


if __name__ == '__main__':

    # Create a dictionary to describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

            'resource' : 'local.summit',
            'queue'    : 'batch',
            'schema'   : 'local',
            'walltime' : 15,
            'cpus'     : 48,
            'gpus'     : 4
    }

    # Create Application Manager
    appman = AppManager()
    appman.resource_desc = res_dict

    p1 = generate_MD_pipeline()
    p2 = generate_ML_pipeline()

    pipelines = []
    pipelines.append(p1)
    pipelines.append(p2)

    # Assign the workflow as a list of Pipelines to the Application Manager. In
    # this way, all the pipelines in the list will execute concurrently.
    appman.workflow = pipelines

    # Run the Application Manager
    appman.run()
