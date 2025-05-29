import gradio as gr
from gpt_handler import call_gpt
from prompt_templates import create_awards_prompt
from resume_state import update_resume

def create_awards_tab(state):
    with gr.Tab("자격증 및 수상"):
        with gr.Column():
            input_text = gr.Textbox(
                label="자격증 또는 수상 내역",
                lines=4,
                placeholder="예: 정보처리기사 자격증 보유, Kaggle 대회 수상 등"
            )
            output_text = gr.Textbox(label="영문 이력서 문장", lines=3)
            convert_btn = gr.Button("변환")

            def handle_awards(role, text, state):
                company = state.get("기업")
                applicant_type = state.get("지원유형")

                prompt = create_awards_prompt(
                    job=role,
                    awards=text,
                    company=company,
                    applicant_type=applicant_type
                )
                result = call_gpt(prompt)
                state = update_resume(state, "자격증 및 수상", result)
                return result, state

            convert_btn.click(
                fn=handle_awards,
                inputs=[gr.Text(label="직무", visible=False), input_text, state],
                outputs=[output_text, state],
                show_progress=True
            )
