import markdown
from markdown.preprocessors import Preprocessor
import re


class PrismCodeExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.preprocessors.register(PrismBlockPreprocessor(md), "prism_code_block", 180)


class PrismBlockPreprocessor(Preprocessor):
    PRISM_BLOCK_RE = re.compile(
        r"(?P<fence>^(?:~{3,}|`{3,}))[ ]*(\{?\.?(?P<lang>[a-zA-Z0-9_+-]*)\}?)?[ ]*\n(?P<code>.*?)(?<=\n)(?P=fence)[ ]*$",
        re.MULTILINE | re.DOTALL,
    )
    BLOCK_WRAP = "<pre><code{0}>{1}</code></pre>"
    LANG_TAG = ' class="language-{0}"'
    CODE_WRAP = '<code class="language-markup">{0}</code>'

    def __init__(self, md):
        super(PrismBlockPreprocessor, self).__init__(md)

    def block_replace(self, text):
        while True:
            m = self.PRISM_BLOCK_RE.search(text)
            if m:
                lang = ' class="language-markup"'
                if m.group("lang"):
                    lang = self.LANG_TAG.format(m.group("lang"))

                block = self.BLOCK_WRAP.format(lang, self._escape(m.group("code")))
                placeholder = self.md.htmlStash.store(block)
                text = "%s\n%s\n%s" % (
                    text[: m.start()],
                    placeholder,
                    text[m.end() :],
                )
            else:
                break
        return text

    def code_replace(self, text):
        while True:
            m = re.search(r"`(?P<code>[^\n^`]+)`", text, re.M)
            if m:
                content = m.group("code")
                code = self.CODE_WRAP.format(content)
                placeholder = self.md.htmlStash.store(code)
                text = "{0}\n{1}\n{2}".format(
                    text[: m.start()], placeholder, text[m.end() :]
                )
            else:
                break
        return text

    def run(self, lines):
        """Match and store Fenced Code Blocks in the HtmlStash."""
        text = self.code_replace(self.block_replace("\n".join(lines)))
        return text.split("\n")

    def _escape(self, txt):
        """basic html escaping"""
        txt = txt.replace("&", "&amp;")
        txt = txt.replace("<", "&lt;")
        txt = txt.replace(">", "&gt;")
        txt = txt.replace('"', "&quot;")
        return txt
