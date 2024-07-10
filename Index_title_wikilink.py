import pywikibot
import re

def find_and_replace_in_wikipedia_pages(input_filename, regex_pattern):
    site = pywikibot.Site('ta', 'wikisource')

    with open(input_filename, 'r', encoding='utf-8') as infile:
        page_titles = [line.strip() for line in infile]

    for title in page_titles:
        page = pywikibot.Page(site, title)
        page_content = page.text

        # Find matches using the regex pattern
        matches = re.findall(regex_pattern, page_content)

        if matches:
            for match in matches:
                # wikilink the title in the Index
                modified_match = f"[[{match}]]"
                page_content = page_content.replace(match, modified_match, 1) #1 is added so that only one replacement is done

            # Save the modified content back to the Wikisource page
            page.text = page_content
            page.save(summary="தலைப்பு விக்கியிணைப்பு", minor=True)
            print(f"Modified content saved to Wikipedia page: {title}")
        else:
            print(f"No matches found for regex pattern in {title}")

if __name__ == "__main__":
    input_filename = "wikisource_pages2.txt"  # Specify the input file containing page titles
    regex_to_find = r"Title=(.*)"  # Replace with your desired regex pattern

    find_and_replace_in_wikipedia_pages(input_filename, regex_to_find)
