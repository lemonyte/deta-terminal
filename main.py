import os
import subprocess

from deta_space_actions import Actions, ActionsMiddleware, Input, InputType, custom_view
from deta_space_actions.actions import HandlerInput
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from models import Command, Result

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
actions = Actions()
app.add_middleware(ActionsMiddleware, actions=actions)
CommandView = custom_view("/static/view.html")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html") as file:
        return HTMLResponse(file.read())


@app.post("/api/command", response_model=Result)
async def command(cmd: Command):
    original_cwd = os.getcwd()
    try:
        os.chdir(cmd.cwd)
        result = subprocess.run(
            cmd.args,
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
        args = cmd.args
    new_cwd = os.getcwd()
    os.chdir(original_cwd)
    return Result(
        stdout=stdout,
        stderr=stderr,
        returncode=returncode,
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
async def command_action(payload: HandlerInput) -> CommandView:
    args = payload.get("command", "").split()
    result = await command(Command(args=args))
    return CommandView(result.model_dump())


# TODO: output and command history using base
