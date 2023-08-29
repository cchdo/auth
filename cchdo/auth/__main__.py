import json

import click

from .session import session as s

CCHDO_API = "https://cchdo.ucsd.edu/api/v1"
CRUISE_API = f"{CCHDO_API}/cruise"
FILE_API = f"{CCHDO_API}/file"


def json_edit_loop(metadata):
    human_json = json.dumps(metadata, indent=2, sort_keys=True)

    try_again = True
    while try_again:
        edited = click.edit(text=human_json, extension=".json")

        if edited is None:
            raise click.Abort()

        try:
            json.loads(edited)
            try_again = False
        except ValueError:
            click.confirm(
                "Edited cruise was not valid json, would you like try fixing?",
                abort=True,
            )
            human_json = edited

    return json.loads(edited)


@click.group()
def cli():
    ...


@cli.command()
@click.argument("apikey")
def apikey(apikey):
    """Write the API key to the config file, creating if needed"""
    from . import CONFIG_FILE, _check_apikey, write_apikey

    try:
        _check_apikey(apikey)
    except ValueError:
        click.echo("The API key provided doesn't look valid")
        raise click.Abort
    write_apikey(apikey)
    click.echo(f"API Key written to {CONFIG_FILE}")


@cli.command()
@click.argument("expocode")
def edit_cruise(expocode):
    """Edit a cruise json in your $EDITOR"""

    cruises = {c["expocode"]: c["id"] for c in s.get(CRUISE_API).json()["cruises"]}
    try:
        cruise_id = cruises[expocode]
    except KeyError:
        raise click.ClickException(f"Cruise not found: {expocode}")

    click.echo(f"Loading cruise {cruise_id}")

    cruise_json = s.get(f"{CRUISE_API}/{cruise_id}").json()

    click.echo("Opening editor")

    edited_metadata = json_edit_loop(cruise_json)

    click.echo(f"PUTting to cruise: {cruise_id}")

    while True:
        r = s.put(f"{CRUISE_API}/{cruise_id}", json=edited_metadata)

        if r.status_code != 201:
            click.echo(f"Error message: {r.text}")
            click.confirm(
                "Edited cruise was rejected by the API, would you like try fixing?",
                abort=True,
            )
            edited_metadata = json_edit_loop(edited_metadata)
            continue

        break

    click.echo("Cruise Edit done!")


@cli.command()
@click.argument("file_id")
def edit_file(file_id):
    """Edit a file json in your $EDITOR

    file_id is the internal id of the file to edit
    """
    click.echo(f"Loading file {file_id}")

    file_json = s.get(f"{FILE_API}/{file_id}").json()

    click.echo("Opening editor")

    edited_metadata = json_edit_loop(file_json)

    click.echo(f"PUTting to file: {file_id}")

    while True:
        r = s.put(f"{FILE_API}/{file_id}", json=edited_metadata)

        if r.status_code != 201:
            click.echo(f"Error message: {r.text}")
            click.confirm(
                "Edited file was rejected by the API, would you like try fixing?",
                abort=True,
            )
            edited_metadata = json_edit_loop(edited_metadata)
            continue

        break

    click.echo("File Edit done!")


if __name__ == "__main__":
    cli()
