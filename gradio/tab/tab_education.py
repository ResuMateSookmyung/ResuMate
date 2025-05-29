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
            convert_btn = gr.Button("변환")

            def handle_education(role, text, state):
                company = state.get("기업")
                applicant_type = state.get("지원유형")

                prompt = create_education_prompt(
                    job=role,
                    education=text,
                    company=company,
                    applicant_type=applicant_type
                )
                result = call_gpt(prompt)
                state = update_resume(state, "학력", result)
                return result, state

            convert_btn.click(
                fn=handle_education,
                inputs=[gr.Text(label="직무", visible=False), input_text, state],
                outputs=[output_text, state],
                show_progress=True
            )