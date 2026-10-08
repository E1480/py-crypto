from rich.console import Console
from rich.panel import Panel
from rich.table import Table

C_SUCCESS = "green"
C_FAIL = "red"
##
    # def success(title: str = "", body: str = "", result: str = "", after: str = ""):
    #     print(
    #         Panel(
    #             f"{body} [{C_SUCCESS}]{result}[/{C_SUCCESS}] {after}",
    #             title=title,
    #             border_style="cyan",
    #             padding=(1, 2),
    #         )
    #     )


    # def fail(title: str = "", body: str = "", result: str = "", after: str = ""):
    #     print(
    #         Panel(
    #             f"{body} [{C_FAIL}]{result}[/{C_FAIL}] {after}",
    #             title=title,
    #             border_style="red",
    #             padding=(1, 2),
    #         )
    #     )

console = Console()

table = Table.grid(padding=(0, 2))

def success(**kwargs: str):

    for k, v in kwargs.items():
        if k == "Verdict":
            v = f"[{C_SUCCESS}]{v}[/{C_SUCCESS}]"
        table.add_row(k, ":", v)

    console.print(
        Panel(
            table,
            title="Hashing Comparison",
            border_style="light_green",
            padding=(1,1)
        )
    )


def fail(**kwargs: str):

    for k, v in kwargs.items():
        if k == "Verdict":
            v = f"[{C_FAIL}]{v}[/{C_FAIL}]"
        table.add_row(k, ":", v)

    console.print(
        Panel(
            table,
            title="Hashing Comparison",
            border_style="red",
            padding=(1,1)
        )
    )
