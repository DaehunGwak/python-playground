import pprint

import web_scrapper.services as scrapper

print("=== engineering ===================================")
for page, jobs in enumerate(scrapper.scrap_job_descriptions()):
    print(f"page: {page + 1}")
    pprint.pp(jobs)
    print()


print("=== skills ========================================")
skills = scrapper.scrap_engineering_popular_skills()
print("popular engineering skills: ")
pprint.pp(skills)

for skill in skills:
    print(f"now skill: {skill}")
    pprint.pp(scrapper.scrap_job_descriptions_by_skill(skill))
    print()
