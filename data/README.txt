TF2 Casual Manager (TF2CM)
==========================

TF2CM is a map selections manager for TF2 casual mode. The map selection of casual mode in TF2 has save/load buttons, but you can have only one save slot. TF2CM can modify this save data out of game, you can create and save many groups of maps as map selections, and apply them to TF2.

TF2CM's UI
----------
* Map Groups: The selection groups list.
* Add: Create a new selection group.
* Delete: Remove the selected group.
* Save: Save data of all groups to TF2CM's config.
* Import from TF2: Import current TF2 map selection from file (click SAVE CURRENT SETTINGS in TF2 first).
* Apply to TF2: Apply map selection of the selected group to the TF2 save file.
* Group: Edit the name of the selected group.
* Map Selection: Change the map selection of the selected group.
* "+" & "-": Expand and collapse map selection tree.
* Right click a map in the tree will show the preview of the map.
* Click the preview image will hide it.

How To Use
----------
1. Click "Add" to create a new selection group.
2. Edit the group name.
3. Select any map you wanna queue.
4. Click "Save" to save changes.
5. Click "Apply to TF2" to apply change to TF2 save file.
6. Click "LOAD SAVED SETTINGS" button in game, this button is on the top-right corner of the Casual Mode menu.
7. Find your casual game as usual.

Tech Details
------------
TF2CM edits casual_criteria.vdf in tf folder, this is the map selection save file, which is a plain text file. It's VAC safe to edit it when TF2 is running.

Source Code
-----------
https://github.com/deluxghost/TF2CasualManager
