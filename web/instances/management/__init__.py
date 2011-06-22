from django.db.models.signals import post_syncdb
from django.db import connection, transaction
import web.instances.models

def instance_post_syncdb(sender, **kwargs):
    cursor = connection.cursor()
    cursor.execute(
"""
CREATE OR REPLACE VIEW instances_instance AS
SELECT instances_instanceview.id, instances_instanceview.name, instances_instanceview.slug, instances_instanceview.start_date, instances_instanceview.end_date,
instances_instanceview.location, instances_instanceview.content, instances_instanceview.curator_id, 
        CASE
            WHEN now() > instances_instanceview.start_date AND now() < instances_instanceview.end_date THEN true
            ELSE false
        END AS is_active, 
        CASE
            WHEN now() > instances_instanceview.end_date THEN true
            ELSE false
        END AS is_expired,
    CASE
        WHEN now() > instances_instanceview.start_date THEN true
        ELSE false
    END AS is_started,
    instances_instanceview.id as instanceview_ptr_id
   FROM instances_instanceview;

--Happy fun insert, update, and delete for the view so that django doesn't even know that it's not a table
CREATE OR REPLACE RULE insert_instance AS
    ON INSERT TO "instances_instance" DO INSTEAD  INSERT INTO instances_instanceview (name, slug, start_date, end_date, location,
content, curator_id)
  VALUES (new.name, new.slug, new.start_date, new.end_date, new.location, new.content, new.curator_id);

CREATE OR REPLACE RULE update_instance AS
    ON UPDATE TO "instances_instance" DO INSTEAD  UPDATE instances_instanceview SET name = new.name, slug = new.slug, start_date = new.start_date, end_date = new.end_date, location = new.location, content = new.content, curator_id = new.curator_id
  WHERE instances_instanceview.id = new.id;

CREATE OR REPLACE RULE delete_instance AS
    ON DELETE TO "instances_instance" DO INSTEAD DELETE FROM instances_instanceview
  WHERE instances_instanceview.id = old.id;
""")
    

post_syncdb.connect(instance_post_syncdb, sender=web.instances.models)
