from flask import Blueprint, current_app
import click
from routes.superuser import create_superuser


blueprint = Blueprint('bash', __name__)


#Bash routes
@blueprint.cli.command('createsuperuser')
@click.argument('name')
@click.argument('password')
def create_su(name, password):
    create_superuser(name, password)
    current_app.logger.info('Superuser created')
    return True