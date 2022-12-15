#!/bin/bash
#SBATCH --job-name=evaluate_vqa
#SBATCH --open-mode=append
#SBATCH --output=evaluate.out
#SBATCH --error=evaluate.err
#SBATCH --export=ALL
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32GB
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=ww2135@nyu.edu

singularity exec --nv --overlay /home/ww2135/env.ext3:ro /home/ww2135/cu.sif bash -c "source /ext3/env.sh; cd run_scripts/vqa; bash evaluate_vqa_beam.sh val"
