# DashboardQA: Benchmarking Multimodal Agents for Question Answering on Interactive Dashboards

<img width="2975" height="1597" alt="DashboardQA Overview" src="https://github.com/user-attachments/assets/2cb3100d-64eb-43c0-b2cf-8548a2324925" />

## 🔗 Quick Links

- 🤗 **Dataset**: https://huggingface.co/datasets/ahmed-masry/DashboardQA  
- 🖥️ **Code**: https://github.com/vis-nlp/DashboardQA  
- 📄 **Paper**: https://arxiv.org/abs/2508.17398  

---

## 📌 Overview

**DashboardQA** is the first benchmark designed to evaluate **multimodal agents** on **interactive dashboard question answering**. Unlike previous chart QA benchmarks that rely on static images, DashboardQA challenges agents to perform **multi-step interactions** across real-world Tableau dashboards, including filtering, tab switching, and coordinated view navigation.

Built on the **OSWorld** environment, DashboardQA supports evaluation of both **open-source** and **closed-source** multimodal agents.

---

## 💾 Installation

> **Note:** This installation guide is tailored for **Google Cloud Platform (GCP)** virtual machines. For other platforms, please consult the [OSWorld repository](https://github.com/xlang-ai/OSWorld) for environment setup instructions.

### Step 1: Launch a GCP VM

Create a virtual machine using the provided script:

```bash
https://github.com/AhmedMasryKU/DashboardQA_Clean/blob/main/launch_gcp_instance.sh
```

**Optional: GPU Instance for Open-Source Models**

If you plan to host open-source models locally, you'll need a GPU-enabled instance. Use this script instead:

```bash
https://github.com/AhmedMasryKU/DashboardQA_Clean/blob/main/launch_gcp_instance_gpu.sh
```

### Step 2: Install Dependencies

SSH into your VM and execute the setup script:

```bash
https://github.com/AhmedMasryKU/DashboardQA_Clean/blob/main/gcp_setup.sh
```

⚠️ **Important:**
- Update the `USER_HOME` variable in the script to match your home directory
- Ensure the username in the final line of the script matches your actual username

**Optional: vLLM Setup for Open-Source Models**

If hosting open-source models locally, run this additional script:

```bash
https://github.com/AhmedMasryKU/DashboardQA_Clean/blob/main/gcp_setup_vllm.sh
```

⚠️ **Requirements:**
- The model must be compatible with vLLM
- Update all paths and variables in the script before execution

---

## 🚀 Running Inference

### Configure Environment Variables

For **closed-source models**, set the following environment variables as needed:

```bash
export OPEN_API_KEY=your_key_here
export OPENAI_API_KEY_CUA=your_key_here
export ANTHROPIC_API_KEY=your_key_here
export GENAI_API_KEY=your_key_here
export GEMINI_API_KEY=your_key_here (from google ai studio)
```

### Execute Inference

Run model inference using the provided script:

```bash
https://github.com/AhmedMasryKU/DashboardQA_Clean/blob/main/gcp_launch_eval.sh
```

You may need to adjust paths, environment variables, and arguments based on your specific setup.

**Key Arguments:**

- `--model-name`: Specify the model to use (e.g., `gpt-4-mini-2025-08-07`)
- `--setup-name`: Choose between `screenshot_a11y_tree` or `screenshot`
- `--results-folder`: Define the path where model outputs will be saved

---

## 📊 Evaluation

After completing inference, evaluate the generated predictions using our evaluation script (adapted from [ChartQAPro](https://github.com/vis-nlp/ChartQAPro)):

```bash
python evaluate_predictions.py --predictions-folder path/to/your/model/outputs --dataset-name ahmed-masry/DashboardQA-v0.5
```

**Arguments:**
- `--predictions-folder`: Path to the folder containing prediction results
- `--dataset-name`: HuggingFace dataset name (e.g., `ahmed-masry/DashboardQA-v0.5`)

---

## 🙏 Acknowledgements

We extend our gratitude to the authors of [OSWorld](https://github.com/xlang-ai/OSWorld), which provided a crucial foundation for the DashboardQA project.

---

## 📄 Citation

If you find this work useful in your research, please consider citing our paper:

```bibtex
@misc{kartha2025dashboardqabenchmarkingmultimodalagents,
      title={DashboardQA: Benchmarking Multimodal Agents for Question Answering on Interactive Dashboards}, 
      author={Aaryaman Kartha and Ahmed Masry and Mohammed Saidul Islam and Thinh Lang and Shadikur Rahman and Ridwan Mahbub and Mizanur Rahman and Mahir Ahmed and Md Rizwan Parvez and Enamul Hoque and Shafiq Joty},
      year={2025},
      eprint={2508.17398},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2508.17398}, 
}
```
