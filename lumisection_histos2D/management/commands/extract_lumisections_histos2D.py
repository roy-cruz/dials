from django.core.management.base import BaseCommand

from runs.models import Run
from lumisections.models import Lumisection
from lumisection_histos2D.models import LumisectionHisto2D 

# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
import pandas as pd

class Command(BaseCommand):
    help = "Extracts lumisections from files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        df   = pd.read_csv(file_path)
        print(df.head())

        lumisection_histos2D = []

        for index, row in df.iterrows():
            run_number  = row["fromrun"]
            lumi_number = row["fromlumi"]
            title       = row["hname"]
            if run_number == 297057:
                print(run_number, lumi_number, title)

                run, _ = Run.objects.get_or_create(run_number=run_number)
                lumisection, _ = Lumisection.objects.get_or_create(run_number= run, ls_number = lumi_number)
            
                lumisection_histo2D = LumisectionHisto2D(
                    run_number = run,
                    ls_number = lumisection,
                    title = title,
                    data = 1.8
                )

                lumisection_histos2D.append(lumisection_histo2D)

        LumisectionHisto2D.objects.bulk_create(lumisection_histos2D)
        print(f'lumisections histos 2D successfully added!')

