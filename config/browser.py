from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class BrowserConfig:
    debug: bool = os.getenv('BROWSER_DEBUG', 'False').lower() == 'true'
    
    @property
    def headless(self) -> bool:
        return not self.debug


    @property
    def slow_mo(self) -> int:
        return 500 if self.debug else 0