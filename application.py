#!/usr/bin/env python

import argparse
import os

from app.app import create_app


def main():
    parser = argparse.ArgumentParser(description="Flask Template")
    parser.add_argument(
        "--port", "-p",
        help="The port to listen on (default 5001)",
        type=int,
        default=5001,
    )
    parser.add_argument(
        "--echo",
        help="Turn on SQLAlchemy query echoing (convenience function to "
             "override the `app.db.postgres.echo` setting in your "
             "settings.yml). To permanently enable echoing, set it in "
             "settings.yml.",
        action="store_true",
    )
    args = parser.parse_args()

    # SQLAlchemy echo overrider.
    os.environ["APP_ECHO"] = str(args.echo)

    application = create_app()

    flask_options = dict(
        host='0.0.0.0',
        port=args.port or 5001,
        threaded=True,
    )

    application.run(**flask_options)

if __name__ == "__main__":
    main()
