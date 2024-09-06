import os


PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..'))
STATEMENT_DIR = os.path.join(PROJECT_DIR, 'statements')
EQUATION_DIR = os.path.join(PROJECT_DIR, 'equations')


def read_statement(filename: str, lang: str) -> str:
    st_text = ""
    with open(os.path.join(STATEMENT_DIR, filename)) as f:
        lFlag = -1
        for line in f:
            if line.strip() == "---":
                if lFlag == 1:
                    break
                lFlag = -1
            elif lFlag == -1:
                lFlag = line.strip() == lang
            elif lFlag == 1:
                st_text += line
    if not st_text:
        raise NotImplementedError(
            f"Theorem statement not found in language - {lang}")
    return st_text