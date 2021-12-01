import uvicorn
from rake.config import RakeSettingsEnvVar
settings = RakeSettingsEnvVar()
from rake.server import app
uvicorn.run(app, host=settings.host, port=int(settings.port))
