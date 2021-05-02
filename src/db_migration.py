# -----------------------------------------------------------
# Migration sctipts for the DB
# -----------------------------------------------------------

# We nee to define some migration scripts with alembic
# https://stackoverflow.com/questions/24622170/using-alembic-api-from-inside-application-code
# https://www.pythoncentral.io/migrate-sqlalchemy-databases-alembic/
# https://stackoverflow.com/questions/39021059/how-to-run-a-migration-with-python-alembic-by-code


import logging
from alembic.config import Config
from alembic import command

#from app_config import AppConfig

LOG = logging.getLogger(__name__)


def get_current_database_version(input_cfg):
    captured_text = []

    def print_stdout(text, *arg):
        nonlocal captured_text
        captured_text.append(text)
    input_cfg.print_stdout = print_stdout
    command.current(input_cfg)
    if not captured_text:
        return None
    else:
        return captured_text[0]


def run_migrations(script_location: str, dsn: str) -> None:
    LOG.info('Running DB migrations in %r on %r', script_location, dsn)
    LOG.info(f'Running DB migrations in {script_location} on {dsn}')
    alembic_cfg = Config()
    # Set the Folder with the migration scripts
    alembic_cfg.set_main_option('script_location', script_location)
    # Set the Path to the DB ->SQLite
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)

    # info about the currently used DB version
    current_db_version = get_current_database_version(alembic_cfg)

    LOG.info(f"Current DB Version is : {current_db_version}")
    # Check if we are already on the head revision or not
    if not current_db_version:
        # TODO: We do not have any version info, what are we doing now ?!
        # Lets just try to upgrade it to the head revision, if that does not work, we need to investigate further !
        try:
            command.upgrade(alembic_cfg, 'head')
        except:
            LOG.error(
                "Database state is unknown, try to identify the current state !!!")
            raise EnvironmentError(
                "Database state is unknown, try to identify the current state !!!")

    else:
        # Check if we have the head revision or not
        if not "head" in current_db_version:
            LOG.info("DB is NOT up to date ...")
            LOG.info("Starting upgrade process ...")
            # Start the upgrade process
            command.upgrade(alembic_cfg, 'head')

        else:
            LOG.info("DB is up to date ...")


if __name__ == "__main__":
    run_migrations(r"D:\Development\Projects\Invoice_Tracking\src\db_migration",
                   r'sqlite:///D:\Development\Projects\Invoice_Tracking\src\db\invoice_database.db')
