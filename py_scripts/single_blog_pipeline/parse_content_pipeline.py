from extractnet import Extractor
from skillNer.skill_extractor_class import SkillExtractor

from py_scripts.data_structures import BlogMetadata
from py_scripts.single_blog_pipeline.utils import (parse_content_article,
                                                   parse_skills_in_paragraph)


def single_blog_pipeline(
    blog: BlogMetadata,
    text_extractor: Extractor,
    skill_extractor: SkillExtractor
):
    """Enrich blog with skills and their occurences.

    Parameters
    ----------
        blog : BlogMetadata
            blog to process.

        text_extractor : Extractor
            Instance of ``extractnet.Extractor`` used to extract raw text
            from blog.

        skill_extractor : SkillExtractor
            Instance of SKillNer ``skillExtractor`` used to annotate skills.

    Note
    ----
        Pipeline inplace-changes ``blog``
    """
    # parse content
    content = parse_content_article(
        blog,
        text_extractor
    )

    # creating parsed_skills and list_occurrences in blog if they don't exist
    blog.setdefault('parsed_skills', [])
    blog.setdefault('list_occurrences', [])

    # loop over paragraphs in parsed content
    for idx, paragraph in enumerate(content.splitlines()):
        # parse skills
        parsed_skills, occurrences = parse_skills_in_paragraph(
            paragraph,
            skill_extractor,
            paragraph_id=f"{blog['id']}-{idx}"
        )

        # enrich blog with skills
        blog['parsed_skills'] += parsed_skills

        # enrich blog with occurrences
        blog['list_occurrences'] += occurrences
