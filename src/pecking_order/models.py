"""Versioned wire and knowledge models. JSON schemas are exported from these models."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Identifier = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_.-]{0,95}$")]
Language = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$")]
Text = Annotated[str, StringConstraints(min_length=1, max_length=4000)]
Scale = Literal[
    "household", "local", "district", "regional", "polity", "imperial", "transregional"
]
Domain = Literal[
    "political", "administrative", "military", "religious", "economic", "kinship",
    "judicial", "educational", "civic", "clandestine", "diplomatic", "fantastic"
]
Evidence = Literal["generic_model", "source_supported", "adapted"]


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Localized(Model):
    """All authored text needs both launch languages; additional languages are welcome."""

    labels: dict[Language, Text]

    @model_validator(mode="after")
    def bilingual(self):
        if not {"en", "fr"} <= self.labels.keys():
            raise ValueError("Both en and fr translations are required")
        return self


class Title(Model):
    labels: dict[Language, Text]
    native: Text | None = None
    language: Language | None = None
    forms: dict[Language, dict[str, Text]] = Field(default_factory=dict)
    translation: Literal["equivalent", "gloss", "loanword"] = "equivalent"

    @model_validator(mode="after")
    def bilingual(self):
        if not {"en", "fr"} <= self.labels.keys():
            raise ValueError("A title must have en and fr labels")
        if bool(self.native) != bool(self.language):
            raise ValueError("Native title and its language must be supplied together")
        return self


class EvidenceRef(Model):
    status: Evidence = "generic_model"
    sources: list[Identifier] = Field(default_factory=list)
    note: Localized

    @model_validator(mode="after")
    def sourced(self):
        if self.status == "source_supported" and not self.sources:
            raise ValueError("Source-supported claims require a source")
        return self


class Power(Model):
    action: Identifier
    domain: Domain
    basis: Literal["de_jure", "de_facto", "ritual", "advisory"]
    scope: Localized
    limits: Localized
    evidence: EvidenceRef


class Rule(Model):
    id: Identifier
    category: Literal[
        "selection", "succession", "tenure", "removal", "eligibility", "membership",
        "inheritance", "residence", "marriage", "decision", "incompatibility", "vacancy"
    ]
    method: Identifier
    description: Localized
    # Declarative integration constraints, never executable scripts.
    parameters: dict[str, str | int | bool | list[str]] = Field(default_factory=dict)
    evidence: EvidenceRef


class Role(Model):
    id: Identifier
    function: Identifier
    label: Localized
    title: Title
    holder: Literal["person", "collective"] = "person"
    min_holders: int = Field(default=0, ge=0)
    max_holders: int | None = Field(default=1, ge=1)
    duties: Localized
    powers: list[Power]
    rules: list[Rule]
    title_evidence: EvidenceRef
    rank: Title | None = None

    @model_validator(mode="after")
    def cardinality(self):
        if self.max_holders is not None and self.min_holders > self.max_holders:
            raise ValueError("min_holders exceeds max_holders")
        return self


class Relation(Model):
    source: Identifier
    target: Identifier
    kind: Literal[
        "reports_to", "advises", "appoints", "removes", "elects", "checks", "represents",
        "member_of", "coordinates", "ritually_legitimizes"
    ]
    evidence: EvidenceRef


class Unit(Model):
    kind: Identifier
    relation: Literal["contains", "federates", "oversees", "affiliates"]
    min_count: int = Field(default=0, ge=0)
    max_count: int | None = Field(default=None, ge=1)
    note: Localized


class Blueprint(Model):
    id: Identifier
    domain: Domain
    label: Localized
    description: Localized
    scales: list[Scale] = Field(min_length=1)
    traits: list[Identifier]
    roles: list[Role] = Field(min_length=1)
    relations: list[Relation]
    units: list[Unit]
    rules: list[Rule]
    evidence: EvidenceRef

    @model_validator(mode="after")
    def graph(self):
        ids = [r.id for r in self.roles]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate role IDs")
        for edge in self.relations:
            if edge.source not in ids or edge.target not in ids:
                raise ValueError("Relation points to an unknown role")
            if edge.source == edge.target:
                raise ValueError("Self relations are unsupported")
        # Only reports_to must be acyclic. Appointment/control cycles are meaningful.
        graph = {rid: [] for rid in ids}
        for edge in self.relations:
            if edge.kind == "reports_to":
                graph[edge.source].append(edge.target)

        def visit(node, path):
            if node in path:
                raise ValueError("Cyclic reporting hierarchy")
            for target in graph[node]:
                visit(target, path | {node})

        for rid in ids:
            visit(rid, set())
        return self


class Source(Model):
    id: Identifier
    title: Text
    publisher: Text
    url: Annotated[str, StringConstraints(pattern=r"^https://")]
    accessed: Annotated[str, StringConstraints(pattern=r"^\d{4}-\d{2}-\d{2}$")]
    locator: Text
    supports: Localized
    limitations: Localized


class Binding(Model):
    template: Identifier
    # Full replacement of named roles, plus explicit additions and removals. Never a deep merge.
    roles: list[Role]
    remove_roles: list[Identifier] = Field(default_factory=list)
    relations: list[Relation] = Field(default_factory=list)
    replace_relations: bool = False
    rules: list[Rule] = Field(default_factory=list)
    traits: list[Identifier] = Field(default_factory=list)
    evidence: EvidenceRef


class Culture(Model):
    id: Identifier
    label: Localized
    aliases: list[Text]
    region: Localized
    period: tuple[int, int]
    description: Localized
    bindings: list[Binding]

    @model_validator(mode="after")
    def interval(self):
        if self.period[0] > self.period[1]:
            raise ValueError("Reversed period")
        if len({b.template for b in self.bindings}) != len(self.bindings):
            raise ValueError("Duplicate cultural binding")
        return self


class Organization(Model):
    kind: Identifier
    scale: Scale
    traits: list[Identifier] = Field(default_factory=list, max_length=20)


class Adaptation(Model):
    kind: Literal["authoritarian", "elective_succession", "hereditary_succession"]
    target_role: Identifier


class Query(Model):
    schema_version: Literal["1.0"] = "1.0"
    culture: Text
    organization: Organization
    role: Identifier | None = None
    as_of: int | None = Field(default=None, ge=-10000, le=10000)
    mode: Literal["historical", "inspired", "generic"] = "historical"
    locale: Language = "fr"
    fallback_locale: Language = "en"
    adaptations: list[Adaptation] = Field(default_factory=list, max_length=8)


class Diagnostic(Model):
    code: Identifier
    message: Localized
    fields: list[str] = Field(default_factory=list)


class Candidate(Model):
    culture: Identifier
    label: Localized
    period: tuple[int, int]
    supported_kinds: list[Identifier]


class CultureContext(Model):
    id: Identifier
    label: Localized
    region: Localized
    period: tuple[int, int]
    description: Localized


class Resolution(Model):
    schema_version: Literal["1.0"] = "1.0"
    kb_version: str
    kb_digest: str
    request: Query
    status: Literal[
        "resolved", "needs_context", "unsupported", "conflict", "role_not_found"
    ]
    culture: CultureContext | None = None
    blueprint: Blueprint | None = None
    selected_roles: list[Identifier] = Field(default_factory=list)
    candidates: list[Candidate] = Field(default_factory=list)
    diagnostics: list[Diagnostic] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    translation_fallbacks: list[str] = Field(default_factory=list)
    display: dict[str, str] = Field(default_factory=dict)


class Dataset(Model):
    version: str
    templates: list[Blueprint]
    cultures: list[Culture]
    sources: list[Source]
    # Broad user labels are explicitly ambiguous, never mapped to a supposedly universal title.
    broad_aliases: dict[str, list[Identifier]]
