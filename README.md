# radical-cybertools
All things RCT 

### Documentation 
* [Ensemble Toolkit](https://radicalentk.readthedocs.io/en/latest/)
* [Ensemble Toolkit Adaptive Execution Examples](https://radicalentk.readthedocs.io/en/latest/adv_examples/adapt_tc.html)
* Workflow [diagram](https://docs.google.com/drawings/d/1vxudWZtKrF6-O_eGLuQkmzMC9T8HbEJCpYbRFZ3ipnw/edit)


### Run Adrian's script in EnTK

#### Prepare the virtual environment in which to run EnTK

* NOTE: This is NOT a conda environment and it is still python 2.7

```
module load py-virtualenv
virtualenv ve/inspire-experiments
. ve/inspire-experiments/bin/activate
git clone git@github.com:radical-cybertools/radical.pilot.git
git checkout experiment/prte_jsrun
git pull
pip install .
radical-stack
pip install radical.entk
```
* After the installation, check that the installed version of RADICAL-Pilot by running the following:  

  ```
  radical-stak
  [...]   
  radical.pilot        : 0.70.3-v0.70.3-144-gdf51bd1@experiment-prte_jsrun
  [...]
  ```

#### Prepare code and data of the two tasks to run

* NOTE: It is assumed that you have the test dataset `test.zip` for the Model-generation.
```
git clone git@github.com:inspiremd/molecular-active-learning.git
git clone git@github.com:inspiremd/Model-generation.git
cp molecular-active-learning /gpfs/alpine/scratch/mturilli1/bip179/
cp Model-generation /gpfs/alpine/scratch/mturilli1/bip179/
mkdir /gpfs/alpine/scratch/mturilli1/bip179/data
cp -r test /gpfs/alpine/scratch/mturilli1/bip179/data
```

#### Prepare the wrappers around the two task to run

* Each wrapper sets up a specific environment for each task to run.

```
git clone git@github.com:inspiremd/radical-inspire.git
cd radical-inspire
mkdir /gpfs/alpine/scratch/mturilli1/bip179/bin/
cp mmgbsa_wrapper.sh /gpfs/alpine/scratch/mturilli1/bip179/bin/
cp run_learner_wrapper.sh /gpfs/alpine/scratch/mturilli1/bip179/bin/
chmod 777 /gpfs/alpine/scratch/mturilli1/bip179/bin/*.sh
```

#### Prepare and execute EnTK
```
. setup_entk.sh
python inspire_skeleton_summit_workflow.py 
```

#### Output example
```
EnTK session: re.session.login2.mturilli1.018140.0007                               
Creating AppManagerSetting up RabbitMQ system                                 ok
                                                                              ok
Validating and assigning resource manager                                     ok
Setting up RabbitMQ system                                                   n/a
                                                                              ok
create pilot manager                                                          ok
submit 1 pilot(s)
        [ornl.summit_prte:336]
                                                                              ok    
Update: All components created
MD state: SCHEDULING
Update: MD.rescoring state: SCHEDULING
Update: MD.rescoring.task.0000 state: SCHEDULING
Update: ML state: SCHEDULING
Update: ML.learning state: SCHEDULING
Update: ML.learning.task.0001 state: SCHEDULING
Update: MD.rescoring.task.0000 state: SCHEDULED
Update: ML.learning.task.0001 state: SCHEDULED
Update: MD.rescoring state: SCHEDULED
Update: ML.learning state: SCHEDULED
                                                                              ok
add 1 pilot(s)                                                                ok
Update: MD.rescoring.task.0000 state: SUBMITTING
Update: ML.learning.task.0001 state: SUBMITTING
submit 2 unit(s)
        ..                                                                    ok
Update: MD.rescoring.task.0000 state: EXECUTED
Update: MD.rescoring.task.0000 state: DONE
Update: MD.rescoring state: DONE
Update: MD state: DONE
Update: ML.learning.task.0001 state: EXECUTED
Update: ML.learning.task.0001 state: DONE
Update: ML.learning state: DONE
Update: ML state: DONE
wait for 1 pilot(s)
                                                                              ok
closing session re.session.login2.mturilli1.018140.0007                        \
close pilot manager                                                            \
wait for 1 pilot(s)
                                                                         timeout
                                                                              ok
session lifetime: 171.1s                                                      ok
All components terminated
wait for 1 pilot(s)
                                                                         timeout
All components terminated
```
