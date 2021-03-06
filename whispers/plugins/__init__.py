from pathlib import Path
from typing import Optional

from whispers.plugins.config import Config
from whispers.plugins.dockerfile import Dockerfile
from whispers.plugins.htpasswd import Htpasswd
from whispers.plugins.jproperties import Jproperties
from whispers.plugins.json import Json
from whispers.plugins.npmrc import Npmrc
from whispers.plugins.pip import Pip
from whispers.plugins.plaintext import Plaintext
from whispers.plugins.pypirc import Pypirc
from whispers.plugins.python import Python
from whispers.plugins.shell import Shell
from whispers.plugins.xml import Xml
from whispers.plugins.yml import Yml


class WhisperPlugins:
    def __init__(self, filename: str):
        """Inits the rules objects. Call pairs() to get results"""
        self.filename = filename
        self.filepath = Path(filename)
        self.filetype = self.filepath.name.split(".")[-1]
        self.plugin = self.load_plugin()

    def load_plugin(self) -> Optional[object]:
        """Loads the correct plugin for a given file"""
        if not self.filepath.exists():
            return None
        elif not self.filepath.is_file():
            return None
        elif self.filepath.stat().st_size < 7:
            return None
        elif self.filetype in ["yaml", "yml"]:
            return Yml()
        elif self.filetype == "json":
            return Json()
        elif self.filetype == "xml":
            return Xml()
        elif self.filetype.startswith("npmrc"):
            return Npmrc()
        elif self.filetype.startswith("pypirc"):
            return Pypirc()
        elif self.filepath.name == "pip.conf":
            return Pip()
        elif self.filetype in ["conf", "cfg", "config", "ini", "env", "credentials"]:
            if self.filepath.open("r").readline().startswith("<?xml "):
                return Xml()
            else:
                return Config()
        elif self.filetype == "properties":
            return Jproperties()
        elif self.filetype.startswith(("sh", "bash", "zsh", "env")):
            return Shell()
        elif self.filepath.name.startswith("Dockerfile"):
            return Dockerfile()
        elif self.filetype.startswith("htpasswd"):
            return Htpasswd()
        elif self.filetype == "txt":
            return Plaintext()
        elif self.filetype == "py":
            return Python()
        return None

    def pairs(self):
        if self.plugin:
            yield from self.plugin.pairs(self.filepath)
