import gradio as gr
from tab.tab_awards import create_awards_tab
from tab.tab_education import create_education_tab
from tab.tab_experience import create_experience_tab
from tab.tab_intro import create_intro_tab
from tab.tab_job import create_job_tab
from tab.tab_preview import create_preview_tab
from tab.tab_projects import create_projects_tab
from tab.tab_skills import create_skills_tab

with gr.Blocks() as demo:
    resume_state = gr.State({})  # 🔹 모든 탭이 공유하는 상태 객체

    with gr.Tabs():
        create_intro_tab(resume_state)
        create_job_tab(resume_state)       # 🔹 상태 전달
        create_education_tab(resume_state) # 🔹 다른 탭에도 동일하게 전달
        create_skills_tab(resume_state)
        create_projects_tab(resume_state)
        create_experience_tab(resume_state)
        create_awards_tab(resume_state)
        create_preview_tab(resume_state)

if __name__ == "__main__":
    demo.launch()
