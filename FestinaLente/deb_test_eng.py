


from FestinaLente.deb.deb_state import AgentDerived, derive_sheep_taxon
from FestinaLente.empirical_data.sheep import SheepTaxon

from typing import TYPE_CHECKING
if TYPE_CHECKING:
      from FestinaLente.deb.deb_agent import SheepAgent


class TestEngine: 
    def __init__(self, day_length: float = 1.0, n_days: int = 1):

            self.taxon: SheepTaxon = SheepTaxon()  # for now, we only have one taxon, so we can ignore the input taxon string and just use the sheep taxon. In the future, we can expand this to support multiple taxa.
            self.derived: AgentDerived = derive_sheep_taxon(self.taxon)
            self.count: int = 0
            self.instance_dict: dict[int, 'SheepAgent'] = {}
            self.length_of_day: float = day_length