# -*- coding: utf-8 -*-
from databases import DatabaseURL, Database

from utils.config import Config

db_url = DatabaseURL(Config.get("database.url"))
db_url = db_url.replace(
    username=Config.get("database.username", required=False),
    password=Config.get("database.password", required=False),
)
conn = Database(db_url)
