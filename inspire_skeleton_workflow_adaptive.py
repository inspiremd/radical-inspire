#!/usr/bin/env python

from radical.entk import Pipeline, Stage, Task, AppManager


CUR_NEW_STAGE = 0
MAX_NEW_STAGE = 3
# MAX_NEW_STAGE = 90


# ------------------------------------------------------------------------------
def generate_MD_pipeline():

    # --------------------------------------------------------------------------
    def func_condition():
        '''
        Adaptive condition
​
        Returns true ultil MAX_NEW_STAGE is reached. MAX_NEW_STAGE is
        calculated to be achievable within the available walltime.
​
        Note: walltime is known but runtime is assumed. MD pipelines might be
        truncated when walltime limit is reached and the whole workflow is
        terminated by the HPC machine.
        '''
        global CUR_NEW_STAGE, MAX_NEW_STAGE

        if CUR_NEW_STAGE < MAX_NEW_STAGE:
            CUR_NEW_STAGE += 1
            s = describe_MD_stages()
            p.add_stages(s)
        else:
            print 'all done (%d == %d)' % (CUR_NEW_STAGE, MAX_NEW_STAGE)

    # --------------------------------------------------------------------------
    def describe_MD_stages():

        # Docking stage
        s1 = Stage()
        s1.name = 'Docking.%d' % CUR_NEW_STAGE

        # Docking task
        t1 = Task()
        t1.executable = ['sleep']
        t1.arguments = ['3']

        # Add the Docking task to the Docking Stage
        s1.add_tasks(t1)

        # MD stage
        s2 = Stage()
        s2.name = 'Simulation.%d' % CUR_NEW_STAGE

        # Each Task() is an OpenMM executable that will run on a single GPU.
        # Set sleep time for local testing
        for i in range(6):
            t2 = Task()
            t2.executable = ['sleep']
            t2.arguments = ['5']

            # Add the MD task to the Docking Stage
            s2.add_tasks(t2)

        # Add post-exec to the Stage
        s2.post_exec = func_condition

        return [s1, s2]

    # --------------------------------------------------------------------------
    p = Pipeline()
    p.name = 'MD'

    s = describe_MD_stages()
    p.add_stages(s)

    return p


# ------------------------------------------------------------------------------
def generate_ML_pipeline():

    p = Pipeline()
    p.name = 'ML'

    s1 = Stage()
    s1.name = 'Generator-ML'

    # the generator/ML Pipeline will consist of 1 Stage, 2 Tasks Task 1 :
    # Generator; Task 2: ConvNet/Active Learning Model
    # NOTE: Generator and ML/AL are alive across the whole workflow execution.
    # For local testing, sleep time is longer than the total execution time of
    # the MD pipelines.

    t1 = Task()
    t1.name = "generator"
    t1.pre_exec  = [
                  # 'module load python/2.7.15-anaconda2-5.3.0',
                  # 'module load cuda/9.1.85',
                  # 'module load gcc/6.4.0',
                  # 'source activate snakes'
                   ]
  # t1.executable = ['python']
  # t1.arguments  = ['/ccs/home/jdakka/tf.py']
    t1.executable = ['sleep']
    t1.arguments  = ['5']
    s1.add_tasks(t1)

    t2 = Task()
    t2.name = "ml-al"
    t2.pre_exec  = [
                  # 'module load python/2.7.15-anaconda2-5.3.0',
                  # 'module load cuda/9.1.85',
                  # 'module load gcc/6.4.0',
                  # 'source activate snakes'
                   ]
  # t2.executable = ['python']
  # t2.arguments  = ['/ccs/home/jdakka/tf.py']
    t2.executable = ['sleep']
    t2.arguments  = ['10']
    s1.add_tasks(t2)

    # Add Stage to the Pipeline
    p.add_stages(s1)

    return p


# ------------------------------------------------------------------------------
if __name__ == '__main__':

    res_dict = {'resource': 'local.localhost',
                # 'queue' : 'batch',
                # 'schema': 'local',
                'walltime': 15,
                'cpus'    : 48,
                'gpus'    : 4}

    appman = AppManager()

    try:
        appman.resource_desc = res_dict

        p1 = generate_MD_pipeline()
        p2 = generate_ML_pipeline()

        appman.workflow = [p1, p2]
        appman.run()

    finally:
        appman.terminate()
