import gradio as gr
from resume_state import format_resume

def create_preview_tab(state):
    with gr.Tab("이력서 미리보기"):
        with gr.Column():
            preview_btn = gr.Button("전체 이력서 보기")
            resume_output = gr.Markdown()
            gr.Textbox(
                value="ⓘ 생성된 문장은 사용자 입력을 기반으로 하며, 실제 사실과 다를 수 있으며 입력한 정보는 저장되지 않습니다.",
                label="",
                lines=1,
                interactive=False
            )

            def handle_preview(s):
                return format_resume(s).replace("\\n", "\n").strip()

            preview_btn.click(
                fn=handle_preview,
                inputs=state,
                outputs=resume_output
            )
