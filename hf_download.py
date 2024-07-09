import os
from huggingface_hub import HfApi


def load_models_from_project(project_name, repo_type, token):
    api = HfApi(
        endpoint="https://hf-mirror.com",  # Can be a Private Hub endpoint.
        token=token,  # Token is not persisted on the machine.
    )
    try:
        return api.list_repo_files(repo_id=project_name, repo_type=repo_type)
    except Exception as e:
        print(f"Error listing files for {project_name}: {str(e)}")
        return []


# Function to download selected models
def download_selected_models(project_name, selected_models, token, save_dir, use_hf_transfer, use_mirror):
    if use_hf_transfer:
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

    if use_mirror:
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

    if not project_name:
        return "请填写要下载的项目。"

    if not selected_models:
        return "请选择要下载的模型。"

    token_option = f"--token {token}" if token else ""

    model_name = project_name.split("/")
    if save_dir:
        if len(model_name) > 1:
            save_path = os.path.join(save_dir, f"models--{model_name[0]}--{model_name[1]}")
        else:
            save_path = os.path.join(save_dir, f"models--{model_name[0]}")
        save_dir_option = f"--local-dir {save_path}"
    else:
        save_dir_option = ""

    for model in selected_models:
        include_option = f"--include {model}" if model else ""
        download_shell = f"huggingface-cli download {token_option} {include_option} --local-dir-use-symlinks False --resume-download {project_name} {save_dir_option}"
        os.system(download_shell)
        print(download_shell)

    return "下载已完成！"
