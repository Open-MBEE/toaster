#!/usr/bin/env python3
"""Pre-flight: check required tool versions before running the tutorial."""

from toaster.bootstrap import provision

if __name__ == "__main__":
    provision()
    print("All tools verified.")
