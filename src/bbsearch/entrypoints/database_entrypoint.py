"""EntryPoint for the creation of the database."""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--data_path",
                    default="/raid/sync/proj115/bbs_data/cord19_v35",
                    type=str,
                    help="The directory path where the metadata.csv and json files are located, "
                         "files needed to create the database")
parser.add_argument("--db_type",
                    default="sqlite",
                    type=str,
                    help="Type of database. Possible values: (sqlite, mysql)")
args = parser.parse_args()


def main():
    """Run database construction."""
    from pathlib import Path
    import getpass
    import sqlalchemy
    from ..database import CORD19DatabaseCreation

    if args.db_type == 'sqlite':
        database_path = '/raid/sync/proj115/bbs_data/cord19_v35/databases/cord19.db'
        if not Path(database_path).exists():
            Path(database_path).touch()
        engine = sqlalchemy.create_engine(f'sqlite:///{database_path}')
    elif args.db_type == 'mysql':
        # We assume the database `cord19_v35` already exists
        mysql_uri = input('MySQL URI:')
        password = getpass.getpass('Password:')
        engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}'
                                          f'@{mysql_uri}/cord19_v35')
    else:
        raise ValueError(f'\"{args.db_type}" is not supported as a db_type.')

    db = CORD19DatabaseCreation(
        data_path=Path(args.data_path),
        engine=engine)
    db.construct()


if __name__ == "__main__":
    main()
