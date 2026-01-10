cd "/home/ahmed_masry_gcpcredits"
USER_HOME="/home/ahmed_masry_gcpcredits"
MINICONDA_PATH="$USER_HOME/miniconda3"
export PATH="$MINICONDA_PATH/bin:$PATH"
source "$MINICONDA_PATH/etc/profile.d/conda.sh"

conda activate osworld
cd OSWorld/

python eval_dataset_gcp.py --model-name 'gpt-5-mini-2025-08-07' --setup-name 'screenshot_a11y_tree' --dataset-name "ahmed-masry/DashboardQA" --results-folder "/home/ahmed_masry_gcpcredits/results_gpt5_mini/"
