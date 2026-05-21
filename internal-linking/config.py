import os

# Google Sheet ID (override via env var SEO_SHEET_ID)
SHEET_ID = os.environ.get("SEO_SHEET_ID", "1wwhKA8qatXaenBe1Mxd5IZi2tAbw8jgxL7u3QjsUeIw")

# Tab names in Google Sheet
ARTICLES_TAB = "Articles"
KEYWORD_MAPPING_TAB = "Keyword Mapping"
INTERNAL_LINKS_TAB = "Internal Links"

# Path to GSC keyword report
GSC_REPORT_PATH = os.environ.get(
    "GSC_REPORT_PATH",
    os.path.join(os.path.dirname(__file__), "..", "data", "gsc", "gsc-top100-report.tsv"),
)

# Matching thresholds
KEYWORD_MATCH_THRESHOLD = 0.05   # min score to map a keyword to an article
LINK_RELEVANCE_THRESHOLD = 0.08  # min Jaccard score to suggest an internal link
MAX_LINKS_PER_SOURCE = 8         # max outgoing link suggestions per article
