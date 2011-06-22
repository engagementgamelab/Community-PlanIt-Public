from django.db.models.signals import post_syncdb
from django.db import connection, transaction
import web.missions.models

def mission_post_syncdb(sender, **kwargs):
    cursor = connection.cursor()
    cursor.execute(
"""
CREATE OR REPLACE VIEW missions_mission AS
SELECT missions_missionview.id, missions_missionview.name, missions_missionview.slug, missions_missionview.start_date, missions_missionview.end_date,
missions_missionview.video, missions_missionview.description, missions_missionview.instance_id, 
        CASE
            WHEN now() > missions_missionview.start_date AND now() < missions_missionview.end_date THEN true
            ELSE false
        END AS is_active, 
        CASE
            WHEN now() > missions_missionview.end_date THEN true
            ELSE false
        END AS is_expired,
        CASE
            WHEN now() > missions_missionview.start_date THEN true
            ELSE false
        END AS is_started,
        missions_missionview.id as missionview_ptr_id
   FROM missions_missionview;

--Happy fun insert, update, and delete for the view so that django doesn't even know that it's not a table
CREATE OR REPLACE RULE insert_instance AS
    ON INSERT TO "missions_mission" DO INSTEAD  INSERT INTO missions_missionview (name, slug, start_date, end_date, video,
description, instance_id)
  VALUES (new.name, new.slug, new.start_date, new.end_date, new.video, new.description, new.instance_id);

CREATE OR REPLACE RULE update_instance AS
    ON UPDATE TO "missions_mission" DO INSTEAD  UPDATE missions_missionview SET name = new.name, slug = new.slug, 
    start_date = new.start_date, end_date = new.end_date, video = new.video, description = new.description, instance_id = new.instance_id
  WHERE missions_missionview.id = new.id;

CREATE OR REPLACE RULE delete_instance AS
    ON DELETE TO "missions_mission" DO INSTEAD DELETE FROM missions_missionview
  WHERE missions_missionview.id = old.id;
""")
    

post_syncdb.connect(mission_post_syncdb, sender=web.missions.models)
