module load python/2.7.15
module load py-virtualenv/16.0.0-py2
module load py-pip/10.0.1-py2
module load vim
module load py-setuptools/40.4.3-py2
. ~/experiments/radical-inspire/ve/instpire-experiments/bin/activate
export RADICAL_PILOT_DBURL="mongodb://mturilli:m7ur1ll1@one.radical-project.org:27017/mturilli" 
export RADICAL_LOG_LVL="DEBUG"
export RADICAL_LOG_TGT="radical.log"
export RADICAL_PROFILE="TRUE"
export RMQ_HOSTNAME="two.radical-project.org"
export RMQ_PORT="33235"

