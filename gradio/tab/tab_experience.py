import gradio as gr
from gpt_handler import call_gpt
from prompt_templates import create_experience_prompt
from resume_state import update_resume

def create_experience_tab(state):
    with gr.Tab("경력"):
        with gr.Column():
            input_text = gr.Textbox(
                label="경력 (기업명, 직무, 업무, 성과 등)",
                lines=4,
                placeholder="정확한 수치나 구체적인 결과를 입력하면 더 신뢰도 높은 이력서 문장이 생성됩니다. (예: 검색 속도를 개선함 → 검색 속도를 25% 개선함) \n전체 작성 예시: 네이버에서 백엔드 개발자로 근무, Spring Boot 기반 REST API 개발, API 응답 속도 30% 개선 및 DB 쿼리 최적화"
            )
            output_text = gr.Textbox(label="영문 이력서 문장", lines=3)
            tip_text = gr.Textbox(label="개선 팁", lines=4)
            gr.Textbox(
                value="ⓘ 생성된 문장은 사용자 입력을 기반으로 하며, 실제 사실과 다를 수 있으며 입력한 정보는 저장되지 않습니다.",
                label="",
                lines=1,
                interactive=False
            )

            convert_btn = gr.Button("변환")

            def handle_experience(text, state):
                #company = state.get("기업")
                #applicant_type = state.get("지원유형")

                prompt = create_experience_prompt(
                    state=state,
                    experience=text
                )
                full_result = call_gpt(prompt)

                # "---" 구분자 기준으로 결과 문장과 팁 분리
                if '---' in full_result:
                    bullet_point, tips = full_result.split('---', 1)
                else:
                    bullet_point = full_result
                    tips = ""

                state = update_resume(state, "경력", bullet_point.strip())
                return bullet_point.strip(), tips.strip(), state

            convert_btn.click(
                fn=handle_experience,
                inputs=[input_text, state],
                outputs=[output_text, tip_text, state],
                show_progress=True
            )
