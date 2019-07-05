import docx

"""
Col span

+----+----+----+----+
|hoge|piyo|foo |bar |
+----+----+----+----+
|baz |    |foo |bar |
+----+----+----+----+
|baz |    |    |bar |
+----+----+----+----+

          |
          V

+----+----+----+----+
|hoge|piyo|    |    |
+----+----+foo +    +
|    |    |    |bar |
+baz +----+----+    +
|    |    |    |    |
+----+----+----+----+

"""
filename = "filename.docx"
doc = docx.Document(filename)

for t in doc.tables:
    for col in range(len(t.columns)):
        for cell in t.column_cells(col):
            text = cell.text
            if text:
                for next_cell in t.column_cells(col)[1:]:
                    next_text = next_cell.text
                    if next_text == text:
                        cell.merge(next_cell)
                        cell.text = text
                    else:
                        continue
doc.save(filename)
