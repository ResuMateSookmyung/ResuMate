def update_resume(state: dict, section: str, content: str) -> dict:
    """
    특정 항목(section)에 대해 GPT 결과(content)를 state에 저장합니다.
    """
    state[section] = content
    return state


def format_resume(state: dict) -> str:
    """
    state에 저장된 각 이력서 항목을 순서대로 정리해서 하나의 문자열로 반환합니다.
    """
    section_order = [
        "학력",
        "경력",
        "프로젝트",
        "기술 스택",
        "자격증 및 수상",
        "자기소개"
    ]

    output = ""
    for section in section_order:
        if section in state:
            output += f"## {section}\\n{state[section]}\\n\\n"

    return output.strip()
