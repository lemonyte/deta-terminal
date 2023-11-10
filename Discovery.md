---
app_name: "Terminal"
title: "Terminal"
tagline: "Access to a Micro's underlying command shell."
theme_color: "#555555"
git: "https://github.com/lemonyte/deta-terminal"
open_code: true
---

Terminal gives you access to a Micro's underlying operating system and file system.
This app was created for debugging purposes, and just out of curiosity.

## Usage

Similar to how you would use a terminal app on your computer, you type commands and view the output.
However, note that the Deta Micro runtime (essentially the AWS Lambda runtime) is very limited, so many commands and executables are not present.
Basic commands like `ls`, `cat`, and `echo` work, but things like `apt` and `curl` are not available.
