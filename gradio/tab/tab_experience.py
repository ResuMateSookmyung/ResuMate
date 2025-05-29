import gradio as gr
from gpt_handler import call_gpt
from prompt_templates import create_experience_prompt
from resume_state import update_resume

def create_experience_tab(state):
    with gr.Tab("경력"):
        with gr.Column():
            input_text = gr.Textbox(
                label="경력",
                lines=4,
                placeholder="기업명, 직무, 업무, 성과 등을 작성해주세요.\n예: 네이버에서 백엔드 개발자로 근무, Spring Boot 기반 REST API 개발, API 응답 속도 30% 개선 및 DB 쿼리 최적화"
            )
            output_text = gr.Textbox(label="영문 이력서 문장", lines=3)
            convert_btn = gr.Button("변환")

            def handle_experience(role, text, state):
                company = state.get("기업")
                applicant_type = state.get("지원유형")

                prompt = create_experience_prompt(
                    job=role,
                    experience=text,
                    company=company,
                    applicant_type=applicant_type
                )
                result = call_gpt(prompt)
                state = update_resume(state, "경력", result)
                return result, state

            convert_btn.click(
                fn=handle_experience,
                inputs=[gr.Text(label="직무", visible=False), input_text, state],
                outputs=[output_text, state],
                show_progress=True
            )
