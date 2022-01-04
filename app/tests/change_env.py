"""Set .env CONFIG to test mode."""
import dotenv
import typer


def change(conf: str) -> None:
    """Set CONFIG env to test or prod.

    :param conf: command line arg [test, prod]
    """
    if conf in ("prod", "test"):
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        dotenv.set_key(dotenv_file, "CONFIG", conf)


if __name__ == "__main__":
    typer.run(change)
