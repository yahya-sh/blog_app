import importlib
from django.apps import apps
from django.core.management.base import BaseCommand
from scripts.seed.registry import SEEDERS, run_all


import importlib
from django.apps import apps


def load_seeders(verbose: bool = False):
    """
    Loads all {app}.seeders modules safely.

    - Silent by default
    - Verbose mode for debugging
    """

    for app_config in apps.get_app_configs():
        module_path = f"{app_config.module.__name__}.seeders"

        try:
            importlib.import_module(module_path)

            if verbose:
                print(f"✔ loaded: {module_path}")

        except ModuleNotFoundError:
            # expected for most apps → ignore silently
            continue

        except Exception as e:
            # real error → always show
            print(f"❌ failed loading: {module_path}")
            print(f"   {e}")

class Command(BaseCommand):
    help = "Run seeders with dependency resolution"

    def add_arguments(self, parser):
        parser.add_argument("--only", nargs="+", default=None)

        load_seeders()
        print("SEEDERS:", [s.app_label for s in SEEDERS])

        for seeder in SEEDERS:
            seeder.add_arguments(parser)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Running seeders..."))

        run_all(**options)

        self.stdout.write(self.style.SUCCESS("Done"))