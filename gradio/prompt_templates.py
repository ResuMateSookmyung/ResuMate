def get_system_prompt() -> str:
    return f"""
    당신은 영문 이력서 작성에 특화된 어시스턴트입니다. 아래 지침을 반드시 따르세요

    - 당신의 역할은 사용자가 영문 이력서를 작성할 수 있도록 돕는 것입니다.
    - 코드블럭이나 이모지 등 텍스트 이외의 요소는 절대 사용하지 마세요. 오직 순수 텍스트만 출력하세요.
    - 사용자가 입력한 직군 및 직무 정보를 기반으로, 해당 역할에 적합한 표현만 선별하거나 재구성하세요.
    - 영문 이력서 작성 관례를 따르세요.
    - 능동형, 주도적인 표현을 사용하세요.
    - 모든 문장의 첫 단어는 대문자로 시작하세요.
    - 동사는 일관되게 과거형으로 작성하세요.
    - 실무 경험, 성과, 결과 중심으로 간결하게 강조하세요.
    - 구체적인 책임 또는 성과를 압축하여 강조하세요.

    - 나이, 인종, 외모, 결혼 여부 등 개인적 특성을 드러내는 표현은 사용하지 마세요.
    - 국적, 종교, 정치 성향과 관련된 표현은 사용하지 마세요.
    - 출신 지역, 소득 수준 등 사회적 지위를 암시하는 표현은 사용하지 마세요.
    - 특정 집단이나 개인을 일반화하는 표현은 사용하지 마세요.
    - 성별 고정 관념이 반영된 표현은 사용하지 마세요.
    - 성적 지향이나 성 정체성과 관련된 편견이 드러나는 표현은 사용하지 마세요.
    """

def get_style_guidance(company: str = "", applicant_type: str = "") -> str:
    company_hint = {
        "Google": """
        - Google은 STAR 기법 기반의 구조적 문제 해결 능력을 강조합니다. 
        - Google 이력서를 작성할 때는 기존 이력서를 그대로 사용하는 대신 참고만 하고 각 지원 직무에 맞게 새롭게 작성해야 합니다. 
        - 직무 설명과 나의 경험 및 역량이 일치하도록 구성하는 것이 중요하며, 수치와 데이터를 활용해 성과를 구체적으로 보여주는 것이 좋습니다. 
        - 프로젝트 경험은 다음 공식을 참고해 명확하게 성과 중심으로 작성하세요. “[X]를 달성했으며, 이는 [Y]로 측정할 수 있으며, [Z]를 수행한 결과입니다.” 
        - 리더십 경험이 있다면 팀 규모나 담당했던 역할의 범위도 함께 명시해야 합니다. 학생이거나 경력이 적은 경우, 관련 수업이나 학교 프로젝트도 포함하면 좋습니다. 
        - 문장은 간결하고 명확하게, 불필요한 내용을 줄이고 핵심에 집중하여 작성해야 합니다.
        """,

        "Microsoft": "Microsoft는 다양성과 고객 중심 표현을 중요시합니다.",
        "Meta": "Meta는 임팩트, 빠른 반복, 수치 중심 표현을 선호합니다.",
        "OpenAI": "OpenAI는 창의적 문제 해결, 협업, 그리고 적응력을 중시하는 표현을 선호합니다.",
        "Apple": "Apple은 정제된 표현과 협업 중심 문장을 선호합니다.",
    }

    type_hint = {
        "신입": "직무 역량과 학습 의지를 중심으로 표현해주세요.",
        "경력": "실제 성과와 수치 중심으로 작성해주세요.",
    }

    result = ""
    if company in company_hint:
        result += company_hint[company]
    if applicant_type in type_hint:
        result += " " + type_hint[applicant_type]

    return result.strip()

def create_job_prompt(state: dict, job_description: str) -> str:
    job = state.get("직무", "")
    company = state.get("기업", "")
    applicant_type = state.get("지원유형", "")
    style = get_style_guidance(company, applicant_type)
    return f"""
    아래 경력 정보를 기반으로 영문 이력서 경력 항목을 작성해줘.

    지원 회사: {company}
    지원 유형: {applicant_type}
    직군: {job}

    아래는 사용자의 경험 설명입니다. 이를 영어 이력서의 불렛 포인트 문장으로 바꿔주세요:
    - 행동 동사로 시작
    - 성과 중심 (수치가 있다면 포함)
    - 한두 문장으로 요약
    - 도구/기술 언급 포함
    - {style}

    입력: {job_description}

    예시 입력: 아마존에서 프론트엔드 개발자로 채팅 기능을 만들었고 React를 썼어요. DAU가 늘었어요.
    예시 출력: Developed a real-time chat feature using React at Amazon, increasing daily active users by 15%.
    """


def create_education_prompt(state: dict, education: str) -> str:
    job = state.get("직무", "")
    return f"""
    아래 학력 정보를 기반으로 영문 이력서 학력 항목을 작성해줘.

    학력: {education}
    직군: {job} 
    아래의 학력 정보를 영어 이력서 문장으로 만들어주세요.  
    - 간결하게 1줄  
    - 학위, 전공, 학교, 졸업 연도 포함  
    - 필요시 GPA나 수상 내역도 포함

    [입력 예]: 서울대학교, 컴퓨터공학과, 2023년 졸업, GPA 4.0

    [출력 예]: B.S. in Computer Science, Seoul National University, GPA 4.0, Feb 2023
    """

def create_experience_prompt(state: dict, experience: str) -> str:
    job = state.get("직무", "")
    company = state.get("기업", "")
    applicant_type = state.get("지원유형", "")
    style = get_style_guidance(company, applicant_type)
    return f"""
    당신은 영문 이력서 경력 항목을 작성하는 어시스턴트입니다.

    직군: {job}
    경력 내용: "{experience}"

    요청:
    - 영어 불렛 포인트 형식
    - 행동 동사로 시작
    - 수치 중심으로 성과 강조
    - {style}

    예시:
    입력: 아마존에서 주문 시스템 개선, SpringBoot로 리팩터링하고 응답속도 개선
    출력: Refactored order system using Spring Boot at Amazon, reducing response time by 30%.
    """

def create_projects_prompt(state: dict, project: str) -> str:
    job = state.get("직무", "")
    style = get_style_guidance(state.get("기업", ""), state.get("지원유형", ""))
    return f"""
    사용자의 직군은 "{job}"입니다.  
    아래는 프로젝트 경험 설명입니다.
    {project}
    영어 이력서의 프로젝트 항목으로 적절하게 요약해주세요.  
    - 프로젝트 목표, 역할, 기술, 성과를 포함  
    - 한두 줄 불렛 포인트

    [입력 예]: 팀 프로젝트로 앱 만들었고, 로그인/회원가입 기능 담당했어요. Firebase 썼고 500명 이상 사용했어요.

    [출력 예]: Built user authentication system using Firebase in a team-based mobile app project, achieving over 500 active users.

    """

def create_skills_prompt(state: dict, skills: str) -> str:
    job = state.get("직무", "")
    style = get_style_guidance(state.get("기업", ""), state.get("지원유형", ""))
    return f"""
    당신은 영문 이력서의 스킬 항목을 정리하는 전문가입니다.

    직군: {job}
    입력 스킬: "{skills}"

    요청:
    - 관련 기술 분류: Programming, Tools, Languages 등
    - 쉼표 또는 리스트로 정리
    - {style}

    예시:
    입력: Python, SQL, Tableau, Git, Linux  
    출력:
    • Programming Languages: Python, SQL  
    • Tools: Tableau, Git, Linux
    """

def create_awards_prompt(state: dict, awards: str) -> str:
    job = state.get("직무", "")
    return f"""
    직군: {job} 

    사용자의 직군은 {job}입니다.
    아래는 자격증 또는 수상 내역입니다.  
    이를 영어 이력서 항목에 넣기 적절한 방식으로 표현해주세요.  
    - 이름, 발급 기관, 연도 포함

    [입력 예]: 정보처리기사, 2022년, 한국산업인력공단

    [출력 예]: Certified Information Processing Engineer, HRD Korea, 2022
    """

def create_preview_prompt(state: dict) -> str:
    return "전체 이력서 내용을 아래 항목에 맞게 요약 출력하세요. 항목마다 줄바꿈 해주세요:\n- Objective\n- Education\n- Experience\n- Projects\n- Skills\n- Awards"


def create_intro_prompt(state: dict, intro: str) -> str:
    job = state.get("직무", "")
    company = state.get("기업", "")
    applicant_type = state.get("지원유형", "")
    style = get_style_guidance(company, applicant_type)
    return f"""
    당신은 영어 이력서의 Objective (자기소개) 문장을 작성하는 AI 어시스턴트입니다.

    [직군]: {job}  
    [지원 회사]: {company}  
    [지원 유형]: {applicant_type}

    아래 사용자의 자기소개 내용을 바탕으로, 이력서 상단에 들어갈 간결한 영어 자기소개 문장을 작성해주세요:

    "{intro}"

    작성 지침:
    - 1문장
    - 능동형 표현
    - 태도, 가치관, 강점이 드러나도록
    - 커리어 목표 또는 성장 의지 포함
    - {style}
    """