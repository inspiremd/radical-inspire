import os
from radical.entk import Pipeline, Stage, Task, AppManager

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') is None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

# This is the portion of the workflow that can run on Summit. Assumptions:
# - This pipeline process a single ligand
# - The docked structures are built and their score is calculated on Rhea
# - The pipeline has two stages, each with one task:
#    1. Ligand parameterization
#    2. Rescoring of docking


def describe_MD_pipline(t2_senv):
    p = Pipeline()
    p.name = 'MD'

    # Ligand parameterization stage
    s1 = Stage()
    s1.name = 'parameterization'

    # ligand parameterization task
    t1 = Task()
    t1.executable = ['sleep']
    t1.arguments = ['30']

    # Add the parameterization task to the parameterization stage
    s1.add_tasks(t1)

    # Add parameterization stage to the pipeline
    p.add_stages(s1)

    # Docking rescroring stage
    s2 = Stage()
    s2.name = 'rescoring'

    # Docking rescroring task
    t2 = Task()
    # t2.pre_exec = t2_senv
    # t2.executable = ['python']
    # t2.arguments = ['1_mmgbsa.py', '-p', '"test"', '-n', '0']
    t2.executable = ['mmgbsa_wrapper.sh']

    # Add the docking rescroring task to the docking rescroring stage
    s2.add_tasks(t2)

    # Add the docking rescroring stage to the pipeline
    p.add_stages(s2)

    return p


if __name__ == '__main__':

    # Project scratch directory
    pdir = '/gpfs/alpine/scratch/mturilli1/bip179/'

    # Execution environemt for task t2 1_mmgbsa.py
    t2_senv = ['source %s/bin/setup.sh' % pdir]

    # Create a dictionary to describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

            'resource' : 'ornl.summit_prte',
            'queue'    : 'batch',
            'schema'   : 'local',
            'walltime' : 15,
            'cpus'     : 40,
            'gpus'     : 4
    }

    # Create Application Manager
    appman = AppManager()
    appman.resource_desc = res_dict

    p = describe_MD_pipline(t2_senv)

    # Assign the workflow as a list of Pipelines to the Application Manager. In
    # this way, all the pipelines in the list will execute concurrently.
    appman.workflow = p

    # Run the Application Manager
    appman.run()
