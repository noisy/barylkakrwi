from django_cron import CronJobBase, Schedule
from barylka_django.crawler import micro_crawler

class CrawlerCronJob(CronJobBase):
    RUN_EVERY_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'crawler.crawler_cron_job'    # a unique code

    def do(self):
        micro_crawler.crawl(None)
        print "cron done!"
