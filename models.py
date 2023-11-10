from pydantic import BaseModel


class Command(BaseModel):
    command: str
    cwd: str = "."


class Result(BaseModel):
    stdout: str
    stderr: str
    returncode: int
    command: str
    args: list[str]
    cwd: str
