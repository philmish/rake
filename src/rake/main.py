import click
import uvicorn
from rake.errors.cli import UnknownStartMode


@click.command(name="up")
@click.option("--mode", default="default", required=True)
def up(mode):
    if mode.lower() == "default":
        from rake.config import RakeSettingsBase
        settings = RakeSettingsBase()
        
    elif mode.lower() in ["env_file", "envfile", "env"]:
        from rake.config import RakeSettingsEnvFile
        settings = RakeSettingsEnvFile()
    elif mode.lower() in ["var", "vars", "envar", "envvars"]:
        from rake.config import RakeSettingsEnvVar
        settings = RakeSettingsEnvVar()
    else:
        raise UnknownStartMode(f"{mode} is not an accaptable start mode.")

    from rake.server import app
    uvicorn.run(app, host=settings.host, port=int(settings.port))        

if __name__ == "__main__":
    up()
