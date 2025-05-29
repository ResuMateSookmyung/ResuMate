import gradio as gr
from prompt_templates import create_job_prompt

def save_job_info(job, corp, job_type, state):
    state["직무"] = job
    state["기업"] = corp
    state["지원유형"] = job_type  # 여기 key 통일
    return f"선택된 직무: {job} | 기업: {corp} | 유형: {job_type}", state

def create_job_tab(state):
    with gr.Tab("지원 정보"):
        with gr.Column():
            job = gr.Dropdown(
                choices=["Software Engineer", "Data Scientist", "Product Manager", "UX Designer"],
                label="지원 직무 선택"
            )
            corp = gr.Dropdown(
                choices=["Google", "Meta", "OepnAI", "Apple", "Microsoft"],
                label="지원 기업 선택"
            )
            job_type = gr.Radio(choices=["신입", "경력"], label="지원 유형")
            btn = gr.Button("정보 저장")
            output = gr.Textbox(label="입력 확인")

            btn.click(
                fn=save_job_info,
                inputs=[job, corp, job_type, state],
                outputs=[output, state]
            )
