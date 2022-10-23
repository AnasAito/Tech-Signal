from typing import TypedDict, List


class ParsedSkill(TypedDict):
    skill_id: str
    skill_name: str
    occurence: str


class BlogMetadata(TypedDict):
    id: str
    title: str
    link: str
    published: str
    parsed_skills: List[ParsedSkill]
