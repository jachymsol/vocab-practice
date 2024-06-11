import uuid
from anvil.tables import app_tables


def generate_guid(user_id):
    app_tables.users.get_by_id(user_id).update(guid=str(uuid.uuid4()))
