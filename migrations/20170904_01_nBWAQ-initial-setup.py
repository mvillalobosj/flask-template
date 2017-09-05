"""
initial setup
"""

from yoyo import step

__depends__ = {}

steps = [
    step(apply="""
CREATE SCHEMA db;
    """,
         rollback="""
DROP SCHEMA db;
    """),
    step(apply="""
CREATE TABLE db.user (
    id SERIAL PRIMARY KEY,
    fname TEXT,
    lname TEXT,
    created TIMESTAMP WITHOUT TIME ZONE
);
    """,
         rollback="""
DROP TABLE db.user;
    """)
]
