from schemas import SearchResult, ResearchPlanner
from tools.search_tool import search_web


BAD_DOMAINS = [
    "youtube.com",
    "instagram.com",
    "facebook.com",
    "tiktok.com",
    "reddit.com",
    "quora.com",
    "pinterest.com",
    "linkedin.com",
    "community-5.com",
    "womanmagazine.com",
    "tours.com",
    "boxerdelgoloso.com",
    "medium.com",
    "dev.to",
    "news.ycombinator.com",
    "substack.com",
    "bing.com"
]


GOOD_DOMAINS = [
    ".gov",
    ".edu",
    "cfr.org",
    "brookings.edu",
    "rand.org",
    "pewresearch.org",
    "foreignaffairs.com",
    "atlanticcouncil.org",
    "carnegieendowment.org",
    "cambridge.org",
    "nato.int",
    "un.org",
    "imf.org",
    "worldbank.org",
    "oecd.org",
    "mckinsey.com",
    "gartner.com",
    "hbr.org",
    "mit.edu",
    "stanford.edu",
    "nature.com",
    "science.org",
    "sciencedirect.com",
    "springer.com",
    "wiley.com",
    "ieee.org",
    "acm.org"
]


def domain_score(link: str):

    score = 0

    for domain in GOOD_DOMAINS:

        if domain in link:
            score += 10

    return score


def searching_agent(plan: ResearchPlanner):

    search_results = []

    for topic in plan.subtopics:

        print(f"Searching for: {topic}")

        search_output = search_web(topic)

        filtered_results = []

        for result in search_output:

            link = result.get("link", "").lower()
            snippet = result.get("snippet", "").strip()

            # Skip empty snippets
            if not snippet:
                continue

            # Skip very short snippets
            if len(snippet) < 80:
                continue

            # Skip Bing ad links
            if "aclick" in link:
                continue

            # Skip low-quality domains
            if any(
                bad_domain in link
                for bad_domain in BAD_DOMAINS
            ):
                continue

            filtered_results.append(result)

        # Prioritize trusted domains
        filtered_results.sort(
            key=lambda r: domain_score(
                r.get("link", "").lower()
            ),
            reverse=True
        )

        # Keep top results
        for result in filtered_results[:8]:

            search_results.append(
                SearchResult(
                    topic=topic,
                    title=result.get("title", ""),
                    source=result.get("link", ""),
                    content=result.get("snippet", "")
                )
            )

    print(
        f"Collected {len(search_results)} search results"
    )

    return search_results