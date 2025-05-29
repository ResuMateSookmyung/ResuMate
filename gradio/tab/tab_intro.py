import gradio as gr
from gpt_handler import call_gpt
from prompt_templates import create_intro_prompt
from resume_state import update_resume

def create_intro_tab(state):
    with gr.Tab("한줄소개"):
        with gr.Column():
            input_text = gr.Textbox(
                label="한줄소개",
                lines=4,
                placeholder="예: 새로운 기술을 빠르게 습득하고 문제 해결에 열정이 있습니다."
            )
            output_text = gr.Textbox(label="영문 한줄소개 문장", lines=3)
            convert_btn = gr.Button("변환")

            def handle_intro(role, text, state):
                company = state.get("기업")
                applicant_type = state.get("지원유형")

                prompt = create_intro_prompt(
                    job=role,
                    intro=text,
                    company=company,
                    applicant_type=applicant_type
                )
                result = call_gpt(prompt)
                state = update_resume(state, "한줄소개", result)
                return result, state

            convert_btn.click(
                fn=handle_intro,
                inputs=[gr.Text(label="직무", visible=False), input_text, state],
                outputs=[output_text, state],
                show_progress=True
            )
