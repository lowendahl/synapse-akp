"""Entry point for `python -m akp_runtime`."""


class Application:
    """Runtime module entry-point wrapper."""

    def run(self) -> None:
        from akp_runtime.consumer.mcp_server import main as consumer_main

        consumer_main()


def main() -> None:
    """Run the runtime module entry point."""
    Application().run()


if __name__ == "__main__":
    main()
