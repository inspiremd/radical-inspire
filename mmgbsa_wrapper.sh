unset PYTHONPATH

export USERNAME="`whoami`"
export EDITOR="emacs -nw"

# Summit
module add cuda/9.2.148 spectrum-mpi/10.3.0.1-20190611

# Envs
export PROJECT="bip179"
export USER_ARCHIVE="/home/$USER"
export PROJECT_HOME="/ccs/proj/$PROJECT"
export MEMBER_WORK="/gpfs/alpine/scratch/$USER/$PROJECT/"
export PROJECT_WORK="/gpfs/alpine/proj-shared/$PROJECT"
export WORLD_WORK="/gpfs/alpine/world-shared/$PROJECT"
export PROJECT_ARCHIVE="/proj/$PROJECT"

# Conda initialize 
__conda_setup="$('/gpfs/alpine/scratch/mturilli1/bip179/miniconda/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/gpfs/alpine/scratch/mturilli1/bip179/miniconda/etc/profile.d/conda.sh" ]; then
        . "/gpfs/alpine/scratch/mturilli1/bip179/miniconda/etc/profile.d/conda.sh"
    else
        export PATH="/gpfs/alpine/scratch/mturilli1/bip179/miniconda/bin:$PATH"
    fi
fi
unset __conda_setup

# docking and mmgbsa env
conda activate openmm101

# Run mmgbsa.py
python ${MEMBER_WORK}/bin/1_mmgbsa.py -p "${MEMBER_WORK}/data/test" -n 0
