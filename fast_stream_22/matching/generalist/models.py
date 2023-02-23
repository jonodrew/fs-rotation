from fast_stream_22.matching import BasePair, Candidate, Role
from fast_stream_22.matching.models import Travel, Clearance
from fast_stream_22.matching.pair import register_scoring_method


class GeneralistCandidate(Candidate):
    def __init__(
        self,
        primary_anchor_seeking: str,
        secondary_anchor_seeking: str,
        dept_pref_1: str,
        dept_pref_2: str,
        dept_pref_3: str,
        dept_pref_4: str,
        dept_pref_5: str,
        travel_requirements: str,
        accessibility: str = None,
        match_pref_1: str = None,
        match_pref_2: str = None,
        **kwargs
    ):
        self.secondment = False
        kwargs["prior_departments"] = kwargs["prior_departments"].replace(" ", ",")
        super().__init__(**kwargs)
        self.primary_anchor = primary_anchor_seeking
        self.secondary_anchor = secondary_anchor_seeking
        self.dept_prefs = {
            self._stringify_department(dept)
            for dept in [
                dept_pref_1,
                dept_pref_2,
                dept_pref_3,
                dept_pref_4,
                dept_pref_5,
            ]
        }
        self.secondment = False
        self.travel_requirements: Travel = Travel.factory(travel_requirements)
        self._fix_previous_departments()

    def _fix_previous_departments(self):
        """
        Scottish and Welsh government are so varied that Candidates can visit them again, so we remove them as a 'prior
        department' if `self.can_relocate` is False

        :return:
        """
        if not self.can_relocate:
            for department in ("wg", "sg"):
                self.prior_departments.discard(department)

    @property
    def year_group(self) -> int:
        return self._year_group

    @year_group.setter
    def year_group(self, year_group: str) -> None:
        if year_group.endswith("m"):
            self.secondment = True
            self._year_group = 2
        else:
            self._year_group = int(year_group)

    @property
    def clearance(self) -> Clearance:
        return super().clearance if self._clearance != Clearance.DV else Clearance.SC


class GeneralistRole(Role):
    def __init__(self, accessibility: str, anchor: str, **kwargs):
        self.secondment = False
        self.secondment_only = False
        if "6m" in kwargs["suitable_for_year_group"]:
            self.secondment = True
            if kwargs["suitable_for_year_group"] == "6m":
                self.secondment_only = True
        kwargs["suitable_for_year_group"] = kwargs["suitable_for_year_group"].replace(
            "6m", "2"
        )
        super().__init__(**kwargs)
        self.accessibility = accessibility
        self.anchor = anchor


class GeneralistPair(BasePair):
    scoring_weights = {**BasePair.scoring_weights, "anchor": 15}

    @register_scoring_method
    def _check_secondment(
        self, candidate: GeneralistCandidate, role: GeneralistRole
    ) -> None:
        self.disqualified = (candidate.secondment and not role.secondment) or (
            role.secondment_only and not candidate.secondment
        )

    @register_scoring_method
    def _check_travel(self, c: GeneralistCandidate, r: GeneralistRole) -> None:
        """
        Disqualify candidates whose travel requirements don't match those in the role

        :param c: the Candidate
        :param r: the Role
        :return: None
        """
        self.disqualified = r.travel_requirements > c.travel_requirements

    @register_scoring_method
    def _check_prior_departments(
        self, c: GeneralistCandidate, r: GeneralistRole
    ) -> None:
        """
        In the Generalist scheme, candidates are disqualified from visiting a department they've previously visited

        :param c: the Candidate
        :param r: the Role
        :return: None
        """
        self.disqualified = r.department in c.prior_departments

    @register_scoring_method
    def _score_department(
        self, candidate: GeneralistCandidate, role: GeneralistRole
    ) -> None:
        if role.department in candidate.dept_prefs:
            self._score += self.scoring_weights["department"]

    @register_scoring_method
    def _score_anchor(self, c: GeneralistCandidate, r: GeneralistRole) -> None:
        if r.anchor in {c.primary_anchor, c.secondary_anchor}:
            self._score += self.scoring_weights["anchor"]
