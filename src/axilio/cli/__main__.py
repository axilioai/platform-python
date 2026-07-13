"""Enable ``python -m axilio.cli``."""

import sys

from ._app import main

if __name__ == "__main__":
    sys.exit(main())
