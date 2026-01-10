cd "/home/ahmed_elmasry24653"
USER_HOME="/home/ahmed_elmasry24653"
MINICONDA_PATH="$USER_HOME/miniconda3"
export PATH="$MINICONDA_PATH/bin:$PATH"
source "$MINICONDA_PATH/etc/profile.d/conda.sh"

conda create -n vllm_env python=3.12 -y
conda activate vllm_env
pip install --upgrade uv
uv pip install vllm --torch-backend=auto

vllm serve "xlangai/Jedi-3B-1080p" --dtype "bfloat16" --trust-remote-code --host 0.0.0.0 --port 8000 --api-key "abc123"