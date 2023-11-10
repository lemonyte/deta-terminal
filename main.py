import os
import shlex
import subprocess

from deta_space_actions import Actions, ActionsMiddleware, DetailView, Input, InputType
from deta_space_actions.actions import HandlerInput
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from models import Command, Result

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
actions = Actions()
app.add_middleware(ActionsMiddleware, actions=actions)
# CommandView = custom_view("/static/view.html")


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    with open("./static/index.html", encoding="utf-8") as file:
        return HTMLResponse(file.read())


@app.post("/api/command", response_model=Result)
async def command(cmd: Command) -> Result:
    original_cwd = os.getcwd()
    args = shlex.split(cmd.command)
    try:
        os.chdir(cmd.cwd)
        result = subprocess.run(
            args=args,
            capture_output=True,
            text=True,
            check=False,
            # shell=True,
        )
        stdout = result.stdout
        stderr = result.stderr
        returncode = result.returncode
        args = result.args
    except Exception as exc:  # pylint: disable=broad-except
        stdout = ""
        stderr = str(exc)
        returncode = 1
    new_cwd = os.getcwd()
    os.chdir(original_cwd)
    return Result(
        stdout=stdout,
        stderr=stderr,
        returncode=returncode,
        command=cmd.command,
        args=args,
        cwd=new_cwd,
    )


@actions.action(
    title="Run command",
    inputs=[
        Input(
            name="command",
            type=InputType.STRING,
            optional=False,
        ),
    ],
)
async def command_action(payload: HandlerInput) -> DetailView:
    result = await command(Command(command=payload.get("command", "")))
    return DetailView(
        text=f"{result.stdout}\n{result.stderr}",
        title=f"{result.cwd}$ {result.command}",
    )
    # return CommandView(result.model_dump())


# TODO: output and command history using base
