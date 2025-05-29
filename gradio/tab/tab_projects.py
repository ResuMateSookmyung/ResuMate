import gradio as gr
from gpt_handler import call_gpt
from prompt_templates import create_projects_prompt
from resume_state import update_resume

def create_projects_tab(state):
    with gr.Tab("프로젝트"):
        with gr.Column():
            input_text = gr.Textbox(
                label="프로젝트",
                lines=4,
                placeholder="프로젝트 설명, 담당 파트, 성과 등을 작성해주세요.\n예: Django 기반 블로그 웹사이트 개발, 로그인/댓글 기능 구현, AWS EC2에 배포, 성과 등"
            )
            output_text = gr.Textbox(label="영문 이력서 문장", lines=3)
            convert_btn = gr.Button("변환")

            def handle_projects(role, text, state):
                company = state.get("기업")
                applicant_type = state.get("지원유형")

                prompt = create_projects_prompt(
                    job=role,
                    project=text,
                    company=company,
                    applicant_type=applicant_type
                )
                result = call_gpt(prompt)
                state = update_resume(state, "프로젝트", result)
                return result, state

            convert_btn.click(
                fn=handle_projects,
                inputs=[gr.Text(label="직무", visible=False), input_text, state],
                outputs=[output_text, state],
                show_progress=True
            )