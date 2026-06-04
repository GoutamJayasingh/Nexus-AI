from agent import choose_tool

print(
    choose_tool(
        "(25 + 17) * 4",
        None
    )
)

print(
    choose_tool(
        "total sales",
        "sales.xlsx"
    )
)

print(
    choose_tool(
        "what is output",
        "sample.py"
    )
)