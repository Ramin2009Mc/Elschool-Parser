from rich.console import Console
from rich.table import Table
import os
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from src.elsParser import Parser


class Elschool:
    def __init__(self):
        self.console = Console()
        self.parser = None


    def show_menu(self):
        self.art()
        self.console.rule('[bold blue]Welcome to Elschool!')
        login = Prompt.ask('[bold green]Enter login')
        password = Prompt.ask('[bold green]Enter password')
        self.console.print('\n[bold yellow]Loading...')
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description="Authorization...", total=None)
            self.parser = Parser({'login': login, 'password': password})
        if not self.parser.session or not self.parser.DIARY_PARAMS:
            self.console.print('[bold red]~ Womp: authorization error! Check your username and password (っ- ‸ – ς)')
            return

        self.clear()
        while True:
            self.console.print('\n[bold cyan]Menu:')
            self.console.print('1. View the report card (grades)')
            self.console.print('2. View your homework')
            self.console.print('3. Save the report card (grades) to an Excel file')
            self.console.print('0. Exit')
            choice = Prompt.ask('[bold]→ ', show_default=False)
            if choice == '1':
                self.show_marks()
            elif choice == '2':
                self.show_homework()
            elif choice == '3':
                self.save_xlsx()
            elif choice == '0':
                self.console.print('[bold green]Good bye (ノ^∇^)')
                break
        

    def art(self):
        picture = """             .--.           .---.        .-.
         .---|--|   .-.     | R |  .---. |~|    .--.
      .--|===|Sa|---|_|--.__| A |--|:::| |~|-==-|==|---.
      |%%|✩₊˚|cu|===| |~~|%%| M |--|   |_|~|CATS|  |___|-.
      |  |⊹𓂃 |ra|===| |==|  | I |  |:::|=| |    |IT|---|=|
      |  | ✮ |  |   |_|__|  | N |__|   | | |    |  |___| |
      |~~|===|--|===|~|~~|%%|~~~|--|:::|=|~|----|==|---|=|
      ^--^---'--^---^-^--^--^---'--^---^-^-^-==-^--^---^-'"""
        print(picture)
    
    def clear(self):
        try:
            os.system("clear")
        except:
            os.system("cls")


    def show_marks(self):
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description="Uploading ratings...", total=None)
            marks = self.parser.get_marks()
        if not marks:
            self.console.print("[bold red]Couldn't get a report card ( ╥﹏╥)")
            return
        table = Table(title="Your report card", show_lines=True)
        table.add_column("SUBJECT", style="bold")
        max_quarters = max((len(m) for m in marks.values()), default=0)
        for i in range(1, max_quarters+1):
            table.add_column(f"AVERAGE SCORE", justify="center")
            table.add_column(f"{i} QUARTER", justify="center")
        for subject, quarters in marks.items():
            row = [subject]
            for q in range(1, max_quarters+1):
                if q in quarters:
                    row.append(quarters[q][0])
                    row.append(quarters[q][1])
                else:
                    row.append('-')
                    row.append('-')
            table.add_row(*row)
        self.console.print(table)


    def show_homework(self):
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description="Uploading homework...", total=None)
            homework = self.parser.get_home_work()
        if not homework:
            self.console.print("[bold red]Сouldn't get homework ‧º·(˚ ˃̣̣̥⌓˂̣̣̥ )‧º·˚")
            return
        for day, lessons in homework.items():
            self.console.rule(f'[bold blue]{day}')
            table = Table(show_lines=True)
            table.add_column("SUBJECT", style="bold")
            table.add_column("HOME WORK", style="")
            for subject, hw in lessons.items():
                table.add_row(subject, hw if hw else '-')
            self.console.print(table)

    
    def save_xlsx(self):
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description="Saving the report card in Excel...", total=None)
            marks = self.parser.get_marks()
            if not marks:
                self.console.print("[bold red]Couldn't get a report card to save .·´¯`(>▂<)´¯`·.")
                return
            self.parser.save_marks_xlsx(marks)
        self.console.print('[bold green]The report card has been successfully saved to the marks folder (｡◕‿◕｡)')