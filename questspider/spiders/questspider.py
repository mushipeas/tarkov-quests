import re
import scrapy

class QuestSpider(scrapy.Spider):
    name = 'questspider'
    start_urls = ['https://escapefromtarkov.gamepedia.com/index.php?title=Special:WhatLinksHere/Quests&limit=500']

    def parse(self, response):
        yield from response.follow_all(css='#mw-whatlinkshere-list > li > a', callback=self.parse_subpage)
        # for subpagelink in response.css('#mw-whatlinkshere-list > li > a::attr(href)').getall():
        #     subpagelink = response.urljoin(subpagelink)
        #     yield scrapy.Request(subpagelink, callback=self.parse_subpage)


    def parse_subpage(self, response):
        pagetype = response.css('#mw-normal-catlinks > ul > li > a::text').get()
        if pagetype == 'Quests':

            min_level = 0
            if response.css('#Requirements::text').get():
                requirements = response.xpath('string(//div[contains(@id,"mw-content-text")]/div/ul)').get().split("\n")
                
                for requirement in requirements:
                    if 'level' in requirement:
                        l_i = requirement.index('level') + 6
                        min_level = int(requirement[l_i:l_i+2].strip())

                ul_shift = 1
            else:
                requirements = None
                ul_shift = 0

            rewards = response.xpath('string(//div[contains(@id,"mw-content-text")]/div/ul[{n}])'.format(n=2+ul_shift)).get().split("\n")
            experience = 0
            for reward in rewards:
                if "EXP" in reward:
                    experience = int(re.sub("[^0-9]", "", reward.split()[0]))
                    break

            metadata = response.css('#va-infobox0-content > td > table:nth-child(3) > tbody > tr > td.va-infobox-label::text').getall() 
            metadata_vals = [a.xpath('string()').get().split(", ") for a in response.css('#va-infobox0-content > td > table:nth-child(3) > tbody > tr > td.va-infobox-content')]

            if "Type" in metadata:
                type_index = metadata.index("Type")
                quest_type = " ".join(metadata_vals[type_index])
            else:
                quest_type = None

            if "Location" in metadata:
                loc_index = metadata.index("Location")
                location = metadata_vals[loc_index]
            else:
                location = None

            if "Given By" in metadata:
                givenby_index = metadata.index("Given By")
                dealer = " ".join(metadata_vals[givenby_index])
            else:
                dealer = None
                

            yield {
                'title': response.css('#firstHeading::text').get(),
                'dealer': dealer,
                'type': quest_type,
                'location': location,
                'min_level': min_level,
                'requirements': requirements,
                'previous': response.css('#va-infobox0-content > td > table:nth-child(5) > tbody > tr:nth-child(4) > td:nth-child(1) > a::text').getall(),
                'leads_to': response.css('#va-infobox0-content > td > table:nth-child(5) > tbody > tr:nth-child(4) > td:nth-child(3) > a::text').getall(),
                'objectives': response.xpath('string(//div[contains(@id,"mw-content-text")]/div/ul[{n}])'.format(n=1+ul_shift)).get().split("\n"),
                'rewards': rewards,
                'exp': experience
            }


#va-infobox0-content > td > table:nth-child(3) > tbody > tr:nth-child(6) > td.va-infobox-label
#va-infobox0-content > td > table:nth-child(3) > tbody > tr:nth-child(6) > td.va-infobox-content > a