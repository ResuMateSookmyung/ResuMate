import gradio as gr
from gpt_handler import call_gpt
from prompt_templates import create_education_prompt
from resume_state import update_resume

def create_education_tab(state):
    with gr.Tab("학력"):
        with gr.Column():
            input_text = gr.Textbox(
                label="학력 정보",
                lines=4,
                placeholder="예: 서울대학교 컴퓨터공학과 졸업, GPA 4.1, 2023년"
            )
            output_text = gr.Textbox(label="영문 이력서 문장", lines=3)
            gr.Textbox(
                value="ⓘ 생성된 문장은 사용자 입력을 기반으로 하며, 실제 사실과 다를 수 있으며 입력한 정보는 저장되지 않습니다.",
                label="",
                lines=1,
                interactive=False
            )
            convert_btn = gr.Button("변환")

            def handle_education(text, state):
                #company = state.get("기업")
                #applicant_type = state.get("지원유형")

                prompt = create_education_prompt(
                    state=state,
                    education=text
                )
                result = call_gpt(prompt)
                state = update_resume(state, "학력", result)
                return result, state

            convert_btn.click(
                fn=handle_education,
                inputs=[input_text, state],
                outputs=[output_text, state],
                show_progress=True
            )