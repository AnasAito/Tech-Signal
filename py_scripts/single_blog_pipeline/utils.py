import warnings
import requests
from typing import List

from extractnet import Extractor
from skillNer.skill_extractor_class import SkillExtractor
from py_scripts.data_structures import BlogMetadata, ParsedSkill, Occurrences


def parse_content_article(
    blog: BlogMetadata,
    text_extractor: Extractor
) -> str:
    """Parse the raw text content of article."""
    link = blog['link']

    raw_html = requests.get(link, timeout=10).text
    results = text_extractor.extract(raw_html)

    try:
        return results['content']
    except:
        warnings.warn(
            f"Unable to extract content from article:\n{link}"
        )


def parse_skills_in_paragraph(
    text: str,
    skill_extractor: SkillExtractor,
    nb_words_chuncks: int = 40,
    paragraph_id: str = "",
) -> List[ParsedSkill]:
    """Parse skills in content.

    Parameters
    ----------
    text : str
        Text from where to parse skills.

    skill_extractor : SkillExtractor
        Instance of SkillExtractor used to annotate skills

    nb_words_chuncks : int, default 40
        Number of words to consider when partionning text.

    paragraph_id : str, default ""
        id used to identified the paragraph and used to build the ids
        of skills and occurrences.

    Return
    ------
        list_parsed_skills : List[ParsedSkill]
            List of parsed skills.

        list_occurrences : List[Occurrence]
            List of skill occurrences.
    """
    # averge word size in english is 5
    list_ptr_chuncks = chunck_content(text, chunck_size=5*nb_words_chuncks)
    list_parsed_skills: List[ParsedSkill] = []
    list_occurrences: List[Occurrences] = []

    # loop over chunks
    for i in range(len(list_ptr_chuncks)-1):
        # select chunck
        chunck = text[list_ptr_chuncks[i]:list_ptr_chuncks[i+1]]

        # extract skills
        annotations = skill_extractor.annotate(
            text=chunck
        )

        # to avoid creating occurrence with no skills
        contains_skill = False
        for type_of_match, match_results in annotations["results"].items():
            for skill in match_results:
                # chunk contains skill
                contains_skill = True

                parsed_skill: ParsedSkill = {
                    "skill_id": skill["skill_id"],
                    "skill_name": skill["doc_node_value"],
                    "occurrence_id": f"{paragraph_id}-{i}",
                }

                list_parsed_skills.append(parsed_skill)

        # add occurrence if it contains skills
        if contains_skill:
            occurrence: Occurrences = {
                "occurrence_id": f"{paragraph_id}-{i}",
                "content": chunck
            }
            list_occurrences.append(occurrence)

    return list_parsed_skills, list_occurrences


def chunck_content(
    content: str,
    chunck_size: int = 200
) -> List[int]:
    """Partion content into chuncks with at most ``chunck_size``.

    Parameters
    ----------
    content : str
        text to partition.

    chunck_size : int, default 200
        Number of caracters in a chunk.

    Return
    ------s
        list_ptr : List[int]
            List of pointer such that content[ptr:ptr+1] delimits a chunck.
    """
    # ptr: pointer
    nb_ptr = len(content) // chunck_size
    list_ptr = []

    ptr = 0
    for _ in range(nb_ptr):
        ptr += chunck_size
        if ptr >= len(content):
            break

        # avoid ptr that splits words
        # ex: "I want to avoid this Fuc" --> "I want to avoid this"
        while content[ptr] != " ":
            ptr -= 1

        list_ptr.append(ptr)

    return [0] + list_ptr + [len(content)]
