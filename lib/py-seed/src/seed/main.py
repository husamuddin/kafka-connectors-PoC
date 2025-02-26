import asyncio
import argparse
from .util import seed, with_connection_string

@with_connection_string('mongodb')
def mongodb_seed(*args):
    asyncio.run(seed(*args))

@with_connection_string('docdb')
def docdb_seed(count, *args):
    asyncio.run(seed(count, *args))

run = {
    "mongodb": mongodb_seed,
    "docdb": mongodb_seed
}

def main():
    parser = argparse.ArgumentParser(
        description="""
        MongoDB and DocDB sample data seeder
        """
    )

    parser.add_argument('-t', '--type', choices=["mongodb", "docdb"], required=True, type=str)
    parser.add_argument('-c', '--count', help="number of records to create", default=200, required=True, type=int)
    args = parser.parse_args()

    if args.type not in ["mongodb", "docdb"]:
        raise Exception(f"--type {args.type} must be mongodb or docdb")

    run[args.type](args.count)


if __name__ == "__main__":
    main()
