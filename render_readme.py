import sys, io, pathlib
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def highlight_code(code, lang, attrs):
    if lang:
        try:
            lexer = get_lexer_by_name(lang)
        except Exception:
            return None
        fmt = HtmlFormatter(nowrap=False)
        return highlight(code, lexer, fmt)
    return None

md = MarkdownIt("commonmark", {"html": True, "linkify": True, "highlight": highlight_code}).enable("table")

base = pathlib.Path(r"D:\Development\Project\PythonAgentProject\code-fixer")
src = base / "README.zh-CN.md"
text = src.read_text(encoding="utf-8")
body = md.render(text)

pyg_css = HtmlFormatter(style="friendly").get_style_defs(".highlight")

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Code-Fixer README (中文)</title>
<style>
  body {{ max-width: 900px; margin: 2rem auto; padding: 0 1.5rem; line-height: 1.7; color: #1f2328; font-family: -apple-system, "Segoe UI", "Microsoft YaHei", Roboto, Helvetica, Arial, sans-serif; }}
  h1,h2,h3,h4 {{ color: #0b5394; border-bottom: 1px solid #e5e7eb; padding-bottom: .3em; margin-top: 1.6em; }}
  a {{ color: #0969da; text-decoration: none; }} a:hover {{ text-decoration: underline; }}
  img {{ max-width: 100%; }}
  blockquote {{ border-left: 4px solid #d29922; background: #fff8e1; margin: 1em 0; padding: .3em 1em; color: #4a4a4a; }}
  code {{ background: #f0f1f3; padding: .15em .35em; border-radius: 4px; font-family: "Cascadia Code", Consolas, monospace; font-size: .9em; }}
  pre {{ background: #f6f8fa; padding: 1em; overflow: auto; border-radius: 6px; }}
  pre code {{ background: transparent; padding: 0; }}
  table {{ border-collapse: collapse; }} th, td {{ border: 1px solid #d0d7de; padding: .4em .7em; }}
  details {{ margin: 1em 0; border: 1px solid #d0d7de; padding: .5em 1em; border-radius: 6px; }}
  summary {{ cursor: pointer; font-weight: 600; }}
  {pyg_css}
</style>
</head>
<body>
{body}
</body>
</html>'''

out = base / "README.zh-CN.html"
out.write_text(html, encoding="utf-8")
print("rendered:", out)
print("bytes:", out.stat().st_size)