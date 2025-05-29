import gradio as gr
from resume_state import format_resume

def create_preview_tab(state):
    with gr.Tab("이력서 미리보기"):
        with gr.Column():
            preview_btn = gr.Button("전체 이력서 보기")
            resume_output = gr.Textbox(label="최종 이력서 결과", lines=20)

            def handle_preview(s):
                return format_resume(s)

            preview_btn.click(
                fn=handle_preview,
                inputs=state,
                outputs=resume_output
            )
