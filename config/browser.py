from dataclasses import dataclass



@dataclass(frozen=True)
class BrowserConfig:
    debug: bool = False

    
    @property
    def headless(self) -> bool:
        return not self.debug


    @property
    def slow_mo(self) -> int:
        return 500 if self.debug else 0