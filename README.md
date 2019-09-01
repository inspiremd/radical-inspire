# radical-cybertools
All things RCT 

### Documentation 
* [Ensemble Toolkit](https://radicalentk.readthedocs.io/en/latest/)
* [Ensemble Toolkit Adaptive Execution Examples](https://radicalentk.readthedocs.io/en/latest/adv_examples/adapt_tc.html)
* Workflow [diagram](https://docs.google.com/drawings/d/1vxudWZtKrF6-O_eGLuQkmzMC9T8HbEJCpYbRFZ3ipnw/edit)


### Run Adrian's script in EnTK

```
module load py-virtualenv
virtualenv ve/inspire-experiments
. ve/inspire-experiments/bin/activate
git clone git@github.com:radical-cybertools/radical.pilot.git
git checkout experiment/prte_jsrun
git pull
pip install .
radical-stack

Check that you have installed:
  radical.pilot        : 0.70.3-v0.70.3-144-gdf51bd1@experiment-prte_jsrun

pip install radical.entk
git clone git@github.com:inspiremd/radical-inspire.git
cd radical-inspire
cp mmgbsa_wrapper.sh /gpfs/alpine/scratch/mturilli1/bip179/bin/
mkdir /gpfs/alpine/scratch/mturilli1/bip179/bin/
chmod 777 /gpfs/alpine/scratch/mturilli1/bip179/bin/mmgbsa_wrapper.sh
mkdir /gpfs/alpine/scratch/mturilli1/bip179/data
cp -r test /gpfs/alpine/scratch/mturilli1/bip179/data
. setup_entk.sh
python inspire_skeleton_summit_workflow.py 

EnTK session: re.session.login4.mturilli1.018140.0006              
Creating AppManagerSetting up RabbitMQ system                ok    
          ok    
Validating and assigning resource manager   ok    
Setting up RabbitMQ systemn/a    
^[[B^[[B^[[B^[[B          ok     
create pilot manager       ok    
submit 1 pilot(s)                
        [ornl.summit_prte:336]   
          ok    
All components created           
Update: MD state: SCHEDULING     
Update: MD.rescoring state: SCHEDULING            
Update: MD.rescoring.task.0000 state: SCHEDULING  
Update: MD.rescoring.task.0000 state: SCHEDULED   
Update: MD.rescoring state: SCHEDULED             
create unit manager/autofs/nccs-svm1_home1/mturilli1/experiments/radical-inspire/ve/inspire-experiments/lib/python2.7/site-packages/pymongo/topology.py:155: UserWarning: MongoClient opened before fork. Create MongoClient
 only after forking. See PyMongo's documentation for details: http://api.mongodb.org/python/current/faq.html#is-pymongo-fork-safe      
  "MongoClient opened before fork. Create MongoClient only "       
        ok      
add 1 pilot(s)             ok    
Update: MD.rescoring.task.0000 state: SUBMITTING  
submit 1 unit(s)
        . ok    
Update: MD.rescoring.task.0000 state: EXECUTED    
Update: MD.rescoring.task.0000 state: DONE        
Update: MD.rescoring state: DONE 
Update: MD state: DONE           
wait for 1 pilot(s)              
          ok    
closing session re.session.login4.mturilli1.018140.0006       \    
close pilot manager         \    
wait for 1 pilot(s)              
     timeout    
          ok    
session lifetime: 182.2s   ok    
All components terminated

```
