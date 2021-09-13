from multibar import ProgressBar, ProgressTemplates


bar = ProgressBar(10, 100)
print(bar.write_progress(**ProgressTemplates.DEFAULT))
print(bar.write_progress(**ProgressTemplates.DEFAULT))
print(bar.write_progress(**ProgressTemplates.DEFAULT))
print(bar.write_progress(**ProgressTemplates.DEFAULT))
bar2 = ProgressBar(10, 100)
print(bar2.write_progress(**ProgressTemplates.ADVANCED))
print(bar2.write_progress(**ProgressTemplates.ADVANCED))
