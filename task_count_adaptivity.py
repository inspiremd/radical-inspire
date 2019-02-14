from radical.entk import Pipeline, Stage, Task, AppManager
import os, sys

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'


# from the 800 compounds we can approximate that 500 new stages 
# need to be created

CUR_NEW_STAGE = 0
MAX_NEW_STAGE = 500

def generate_MD_pipeline():

    def func_condition():

        global CUR_NEW_STAGE, MAX_NEW_STAGE

        if CUR_NEW_STAGE <= MAX_NEW_STAGE:
            return True

        return False

    def func_on_true():

        global CUR_NEW_STAGE

        CUR_NEW_STAGE += 1

        s = Stage()

        # each Task() is an OpenMM executable that will run on a single GPU
        # Given limitation on Summit, we can only execute 4 pipelines 
        # The Head Pipeline will consist of 1 Stage, 2 Tasks: Generator and ML/AL 
        # The remaining 3 Pipelines will be devoted to executing simulations 
        # Each simulation Pipeline can execute up-to 6 OpenMM executables 
        
        for i in range(6):
            t = Task()
            t.executable = ['sleep']
            t.arguments = [ '30']

            s.add_tasks(t)

        # Add post-exec to the Stage
        s.post_exec = {
                        'condition': func_condition,
                        'on_true': func_on_true,
                        'on_false': func_on_false
                    }

        p.add_stages(s)

    def func_on_false():
        print 'Done'

    # Create a Pipeline object
    p = Pipeline()

    # Create a Stage object
    s1 = Stage()

    for i in range(6):

        t1 = Task()
        t1.executable = ['sleep']
        t1.arguments = [ '30']

        # Add the Task to the Stage
        s1.add_tasks(t1)

    # Add post-exec to the Stage
    s1.post_exec = {
                        'condition': func_condition,
                        'on_true': func_on_true,
                        'on_false': func_on_false
                    }

    # Add Stage to the Pipeline
    p.add_stages(s1)

    return p

def generate_ML_pipeline():

    # Create a Pipeline object
    p = Pipeline()

    # Create a Stage object
    s1 = Stage()

    # the generator/ML Pipeline will consist of 1 Stage, 2 Tasks
    # Task 1 : Generator, Task 2: ConvNet/Active Learning Model

    t1 = Task()
    t1.executable = ['sleep']
    t1.arguments = ['30']
    s1.add_tasks(t1)

    t2 = Task()
    t2.executable = ['sleep']
    t2.arguments = ['30']
    s1.add_tasks(t2)

    # Add Stage to the Pipeline
    p.add_stages(s1)

    return p


if __name__ == '__main__':

    # Create a dictionary describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

            'resource': 'local.localhost',
            'walltime': 15,
            'cpus': 2,
    }


    # Create Application Manager
    appman = AppManager()
    appman.resource_desc = res_dict

    p1 = generate_MD_pipeline()
    p2 = generate_ML_pipeline()

    pipelines = []
    pipelines.append(p1)
    pipelines.append(p2) 

    # Assign the workflow as a list of Pipelines to the Application Manager
    appman.workflow = [pipelines]

    # Run the Application Manager
    appman.run()