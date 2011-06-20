from django.db.models.signals import post_syncdb
from django.db import connection, transaction
import web.instances.models

def challenge_post_syncdb(sender, **kwargs):
    cursor = connection.cursor()
    cursor.execute(
"""
CREATE OR REPLACE VIEW challenges_challenge AS
SELECT challenges_challengeview.id, challenges_challengeview.map, challenges_challengeview.name, challenges_challengeview.description, challenges_challengeview.start_date, challenges_challengeview.end_date, challenges_challengeview.flagged, challenges_challengeview.instance_id, challenges_challengeview.user_id, challenges_challengeview.game_type, 
        CASE
            WHEN now() > challenges_challengeview.start_date AND now() < challenges_challengeview.end_date THEN true
            ELSE false
        END AS is_active, 
        CASE
            WHEN now() > challenges_challengeview.end_date THEN true
            ELSE false
        END AS is_expired
   FROM challenges_challengeview;

--Happy fun insert, update, and delete for the view so that django doesn't even know that it's not a table
CREATE OR REPLACE RULE insert_challenge AS
    ON INSERT TO "challenges_challenge" DO INSTEAD  INSERT INTO challenges_challengeview (map, name, description, start_date, end_date, flagged, instance_id, user_id, game_type) 
  VALUES (new.map, new.name, new.description, new.start_date, new.end_date, new.flagged, new.instance_id, new.user_id, new.game_type);

CREATE OR REPLACE RULE update_challenge AS
    ON UPDATE TO "challenges_challenge" DO INSTEAD  UPDATE challenges_challengeview SET map = new.map, name = new.name, description = new.description, start_date = new.start_date, end_date = new.end_date, flagged = new.flagged, instance_id = new.instance_id, user_id = new.user_id, game_type = new.game_type
  WHERE challenges_challengeview.id = new.id;

CREATE OR REPLACE RULE delete_challenge AS
    ON DELETE TO "challenges_challenge" DO INSTEAD  DELETE FROM challenges_challengeview
  WHERE challenges_challengeview.id = old.id;
""")
    

post_syncdb.connect(challenge_post_syncdb, sender=web.challenges.models)
