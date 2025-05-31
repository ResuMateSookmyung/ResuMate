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
            gr.Textbox(
                value="ⓘ 생성된 문장은 사용자 입력을 기반으로 하며, 실제 사실과 다를 수 있으며 입력한 정보는 저장되지 않습니다.",
                label="",
                lines=1,
                interactive=False
            )
            convert_btn = gr.Button("변환")

            def handle_intro(text, state):
                #company = state.get("기업")
                #applicant_type = state.get("지원유형")

                prompt = create_intro_prompt(
                    state=state,
                    intro=text
                )
                result = call_gpt(prompt)
                state = update_resume(state, "한줄소개", result)
                return result, state

            convert_btn.click(
                fn=handle_intro,
                inputs=[input_text, state],
                outputs=[output_text, state],
                show_progress=True
            )
