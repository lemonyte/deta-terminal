from pydantic import BaseModel


class Command(BaseModel):
    args: list[str]
    cwd: str = "."


class Result(BaseModel):
    stdout: str
    stderr: str
    returncode: int
    args: list[str]
    cwd: str
