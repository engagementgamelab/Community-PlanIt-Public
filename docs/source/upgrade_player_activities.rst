############
Upgrade instructions for player_activities to challenges apps
############


rename some columns
-------------------

ALTER TABLE player_activities_playeractivity_attachment RENAME COLUMN playeractivity_id TO challenge_id;

update stream_actions table
--------------------------

ALTER TABLE stream_action RENAME action_object_playeractivity_id COLUMN TO action_object_challenge_id;
ALTER TABLE stream_action RENAME COLUMN target_playeractivity_id TO target_challenge_id;
ALTER TABLE stream_action RENAME COLUMN action_object_playermapactivity_id TO action_object_mapchallenge_id;
ALTER TABLE stream_action RENAME COLUMN target_playermapactivity_id TO target_mapchallenge_id;
ALTER TABLE stream_action RENAME COLUMN action_object_playerempathyactivity_id TO action_object_empathychallenge_id;
ALTER TABLE stream_action RENAME COLUMN target_playerempathyactivity_id TO target_empathychallenge_id;

