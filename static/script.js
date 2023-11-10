async function sendCommand(command) {
    command = command.trim();
    if (!command) {
        return;
    }
    const args = command.split(" ");
    if (!args) {
        return;
    }
    if (args[0] == "clear") {
        output.innerHTML = "";
        return;
    }
    // if (args[0] == "cd" && args.length > 1) {
    //     cwd = args[1];
    // }
    const response = await fetch("/api/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            command,
            cwd,
        }),
    })
    return await response.json();
}

function updateScreen() {
    promptLocation.innerText = cwd;
    stdin.innerHTML = currentInput;
    hiddenInput.value = currentInput;
    cursor.innerText = " ".repeat(
        promptLocation.innerText.length
        + promptSeparator.innerText.length
        + hiddenInput.selectionStart
    ) + "_";
    document.scrollingElement.scrollTop = document.scrollingElement.scrollHeight;
    document.scrollingElement.scrollLeft = inputLine.scrollWidth - output.clientWidth;
}

function print(stdout = "", stderr = "") {
    const resultLine = document.createElement("span");
    const stdoutElement = document.createElement("span");
    stdoutElement.classList.add("stdout");
    stdoutElement.innerText = stdout;
    const stderrElement = document.createElement("span");
    stderrElement.classList.add("stderr");
    stderrElement.innerText = stderr;
    resultLine.appendChild(stdoutElement);
    resultLine.appendChild(stderrElement);
    output.appendChild(resultLine);
    output.appendChild(document.createElement("br"));
}

function onInput() {
    currentInput = hiddenInput.value;
    updateScreen();
}

async function onKeyup(event) {
    if (event.key == "ArrowUp" && historyPos > 0) {
        historyPos--;
        currentInput = commandHistory[historyPos];
    }
    else if (event.key == "ArrowDown") {
        if (historyPos < commandHistory.length - 1) {
            historyPos++;
            currentInput = commandHistory[historyPos];
        }
        else {
            currentInput = "";
        }
    }
    else if (event.key == "Escape") {
        currentInput = "";
    }
    else if (event.key == "Enter") {
        const line = document.createElement("span");
        line.innerHTML = inputPrompt.outerHTML + stdin.outerHTML;
        output.appendChild(line);
        output.appendChild(document.createElement("br"));
        if (currentInput.length > 0) {
            inputLine.style.visibility = "hidden";
            commandHistory.push(currentInput);
            historyPos = commandHistory.length;
            const result = await sendCommand(currentInput);
            if (result) {
                print(result.stdout, result.stderr);
                cwd = result.cwd;
            }
            inputLine.style.visibility = "visible";
        }
        currentInput = "";
    }
    updateScreen();
}

async function init() {
    const result = await sendCommand("echo");
    cwd = result.cwd;
    updateScreen();
    hiddenInput.focus();
}

const terminal = document.getElementById("terminal");
const output = document.getElementById("output");
const hiddenInput = terminal.getElementsByClassName("hidden-input")[0];
const inputLine = document.getElementById("input-line");
const inputPrompt = inputLine.getElementsByClassName("prompt")[0];
const promptLocation = inputPrompt.getElementsByClassName("prompt-location")[0];
const promptSeparator = inputPrompt.getElementsByClassName("prompt-separator")[0];
const stdin = inputLine.getElementsByClassName("stdin")[0];
const cursor = inputLine.getElementsByClassName("cursor")[0];

let currentInput = "";
let commandHistory = [];
let historyPos = 0;
let cwd = ".";

window.addEventListener("load", init);
hiddenInput.addEventListener("keyup", onKeyup);

hiddenInput.addEventListener("focusin", () =>{
    cursor.hidden = false;
});

hiddenInput.addEventListener("focusout", () => {
    cursor.hidden = true;
});

// TODO
// fix text selection
// other shells like python, pwsh
