from typing import TypedDict, List


class ParsedSkill(TypedDict):
    skill_id: str
    skill_name: str
    occurrence_id: str


class Occurrences(TypedDict):
    occurrence_id: str
    content: str


class BlogMetadata(TypedDict):
    id: str
    title: str
    link: str
    published: str
    list_occurrences: List[Occurrences]
    parsed_skills: List[ParsedSkill]
