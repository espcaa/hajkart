from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Confirm
from time import sleep
import os
import shutil

sprig = False
loop = False

files = [f"task {n}" for n in range(1, 11)]
console = Console()
doSaving = False


def copydir(dest):
    try:
        shutil.copytree(file, port + dest)
    except FileExistsError:
        shutil.rmtree(port + dest)
        shutil.copytree(file, port + dest)


console.print("[bold blue]Welcome to the IncrPodometer software uploader[/bold blue]")
while True:
    f = open("upload_settings.txt", "r")
    port = Prompt.ask(
        "[italic]Enter the directory of your board ( /run/media/{user}/CIRCUITPY/ on Fedora)[/italic]",
        default=f.read(),
    )
    f.close()
    console.print()
    if os.path.exists(port + "boot_out.txt"):
        console.print("[bold green]Device found ![/bold green]")
        console.print()
        f = open("upload_settings.txt", "r")
        if f.read() != port:
            doSaving = Confirm.ask(
                "Do you want to save this device ? (The next time you'll just have to hit enter)"
            )
        f.close()
        if doSaving:
            f = open("upload_settings.txt", "w")
            f.write(port)
            f.close()
        files = ["main.py"]
        with console.status("[bold green] Moving files ...") as status:
            while files:
                file = files.pop(0)
                if file == "main.py":
                    shutil.copyfile(file, port + "code.py")
                elif file == "lib" or file == "assets":
                    copydir(file)
                else:
                    shutil.copyfile(file, port + file)

                console.log(f"{file} moved")
            break
    else:
        console.print("[bold red]Device not found :confused: [/bold red]")
