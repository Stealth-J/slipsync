from django.core.management.base import BaseCommand
from ssync.models import Tournament
import json
import re

class Command(BaseCommand):
    help = "Populate Market model from Markets.md"

    def handle(self, *args, **options):
        def replace_query(stri):
            sec_regex = r'\((.*)\)'

            regex = r'\s-\s\(.*?\)'
            result_name = re.sub(regex, '', stri)
            result_id = re.search(sec_regex, stri).group(1)

            return result_name, result_id
        
        with open('sites_json/country.txt', 'r', encoding="utf-8") as f:
            content = f.read()
            countries = content.split('\n\n\n')
            for country_block in countries:
                lines = country_block.strip().splitlines()

                if not lines:
                    continue

                # country name is after the leading ||
                country_name = lines[0].replace("||", "").strip().capitalize()

                # remaining lines belong to tournaments
                tournaments = "\n".join(lines[1:]).split("\n\n")

                for tourney in tournaments:
                    parts = tourney.strip().splitlines()
                    if len(parts) != 2:
                        continue

                    b9, sporty = parts

                    # pick whichever is available (if b9 == none, fallback to sporty, etc.)
                    chosen_id = None
                    if b9 != "none":
                        _, chosen_id = replace_query(b9)
                    elif sporty != "none":
                        _, chosen_id = replace_query(sporty)

                    if not chosen_id:
                        continue

                    # update matching tournaments by id
                    qs = Tournament.objects.filter(b9_id = chosen_id) | Tournament.objects.filter(sporty_id = chosen_id)
                    if qs.exists():
                        qs.update(country = country_name)


                            
                        







































































                # with open('sites_json/country.txt', 'r', encoding ="utf-8") as f:
                #     content = f.read()
                #     countries = content.split('\n\n\n')

                #     tourney_objs = []

                #     for country in countries:
                #         tourneys = country.split('\n\n')
                #         for tourney in tourneys:
                #             b9, sporty = tourney.splitlines()
                #             if b9 != 'none':
                #                 b9_name, b9_id = replace_query(b9)
                #             else:
                #                 b9_name, b9_id = None, None
                #             if sporty != 'none':
                #                 sporty_name, sporty_id = replace_query(sporty)
                #             else:
                #                 sporty_name, sporty_id = None, None

                #             tourney_objs.append(
                #                 Tournament(b9_id = b9_id, sporty_id = sporty_id, b9_name = b9_name, sporty_name = sporty_name)
                #             )

                #     Tournament.objects.bulk_create(tourney_objs)

                    