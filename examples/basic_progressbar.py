import multibar

writer = multibar.ProgressbarWriter()
assert writer.write(50, 100, length=6) == "+++---"  # Base signature
