# TAPAS (Telescope Assisted Pointing and Alignment System):
Tapas is a asistance to point to any coordinates of the night sky.
It was desingned to telescopes with camera and ecuatorial mount but without goto system.
The firsts versions suposed that the telescope is properly setted it, horizontanly set, north pointing and right latitude set it.

You must to set the coordinates that you want to point.
TAPAS take a photo shooted and upload to (http://nova.astrometry.net)[Astronmetry.net].
Wait for a response and show in a terminal the coordinates of the central pixel of the photo.
TAPAS with you too the degrees that you need to corrected in each axis RA and DEC (in degrees for both)
Even if you know the relation bewteen a full turn over of the slow motion control and degrees it can give you the amount of turn oven of yours controls.

The feature of help to alignment or to correct the bias is not implemented and is a future goal.

ToDo:

- Create funtions for easy reading.
- Clean and improve the view of the returned info.
- The defoult option must use the last file storaged in the pre-observation folder.
- Create arguments options to take a file or a groups of files.
  -- Groups of files required a log track.

Done: 

- Translate text to english.
