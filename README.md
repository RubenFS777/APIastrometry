# TAPAS (Telescope Assisted Pointing and Alignment System):
TAPAS is an assistance tool for pointing to any coordinates in the night sky. It was designed for telescopes with a camera and an equatorial mount but without a goto system. The initial versions assume that the telescope is properly set up, with a horizontal alignment, pointing north, and the correct latitude set.

You need to set the coordinates you want to point to. TAPAS takes a photo and uploads it to [Astronmetry.net](http://nova.astrometry.net). It then waits for a response and displays the coordinates of the central pixel of the photo in the terminal. TAPAS also provides you with the amount of correction needed in each axis (RA and DEC) in degrees.

Even if you know the relationship between a full turn of the slow-motion control and degrees, TAPAS can calculate the amount of turn needed for your controls.

The feature to assist with alignment or correct bias is not implemented yet but is a future goal.

ToDo:

- Create functions for easier reading.
- Clean and improve the appearance of the returned information.
- The default option should use the last file stored in the pre-observation folder.
- Add options for taking a single file or a group of files as arguments.
  -- Groups of files will require a log track.

Done:

- Translated text to English.
