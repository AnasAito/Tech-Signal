from extractnet import Extractor
from skillNer.skill_extractor_class import SkillExtractor

from py_scripts.data_structures import BlogMetadata
from py_scripts.single_blog_pipeline.utils import (parse_content_article,
                                                   parse_skills)


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
        Pipeline inplace change ``blog``
    """
    # parse content
    content = parse_content_article(
        blog,
        text_extractor
    )

    # parse skills
    parsed_skills = parse_skills(
        content,
        skill_extractor
    )

    # enrich blog
    blog['parsed_skills'] = parsed_skills
