from alembic.command import downgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory

from test.test_fixtures import *


def get_revisions():
    revisions_dir = ScriptDirectory.from_config(get_alembic_config())
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)

    downgrade(alembic_config, revision.down_revision or "-1")
    upgrade(alembic_config, revision.revision)
