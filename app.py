import gradio as gr

from hf_download import load_models_from_project, download_selected_models


# Function to update the model checkboxes based on the project name
def update_model_checkboxes(project_name, token):
    models = load_models_from_project(project_name, "Model", token)
    if models:
        return gr.update(choices=models)
    else:
        return gr.update(choices=[], label="未找到模型，请检查项目名称")


# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# HuggingFace 下载加速器")

    project_name = gr.Textbox(label="项目名称", placeholder="例如：baichuan-inc")
    token = gr.Textbox(label="访问令牌", placeholder="例如：hf_*****")
    save_dir = gr.Textbox(label="保存目录", placeholder="下载后保存的路径")
    use_hf_transfer = gr.Checkbox(label="使用HF Transfer", value=True)
    use_mirror = gr.Checkbox(label="使用镜像站点", value=True)

    load_models_button = gr.Button("加载模型")
    model_checkboxes = gr.CheckboxGroup(label="选择要下载的模型")

    load_models_button.click(fn=update_model_checkboxes, inputs=[project_name, token], outputs=model_checkboxes)

    download_button = gr.Button("下载")
    output = gr.Textbox(label="输出")

    download_button.click(download_selected_models,
                          [project_name, model_checkboxes, token, save_dir, use_hf_transfer, use_mirror],
                          output)

demo.launch()
