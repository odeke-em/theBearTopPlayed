

TheBearTopPlayed:
=================

Project to extra data on songs played throughout the day by Edmonton Radio Station

  [The BearRocks](http://thebearrocks.com).

Each song played is posted in the form of the time of play, title, artist, artistUrl.


History:
========

  This project was inspired by a friend [Konrad Lindenbach](https://github.com/klindenbach)

  who in the past would download from [The BearRocks](http://thebearrocks.com), at the end of

  every week, a list of the top played tracks so as to keep in sync with the latest rock music. 

  About 2.5 years ago, they stopped posting ranked lists and resorted to the new style of a 

  summary per track played during the day.

  Such summaries can be found [here](http://www.thebearrocks.com/broadcasthistory.aspx).

  My job is to restablish this functionality for him and other people that may list posted.

Functionality:
==============
  This project consists of the data extractor in the form of a scrapper/crawler.
  
   Extracted data is then fed into a Database Liason (dbLiason) which then stores the data.

   Simple idea, right?


Code Setup:
===========
  In order to make the data usable for other purposes eg web apps, I found the desire to create

  a dump in the form of JSON objects. To achieve this there are two options:

  + 1. Direct SQL object <=> JSON conversation:

      Basically extracts data at the end of a period of collection, bundles it in \*.json files,
    
      creates a rank file ie most popular tracks first in a \*.rk, then archives these files
  
      and places them in a \*.tar file. Note that this only happens automatically at the end
  
      of a collection period, or if you explicitly run the code that does the final archive.

      To access this setup goto

	[directSQLToJSONLinked](https://github.com/odeke-em/theBearTopPlayed/directSQLToJSONLinked)


  + 2. RestAssured Linked <=> JSON ready:

      This just contains a hook to an api (that I created and continue to work on), for one to hook

      into their Django project/web app to enable json serialization and other features, called

	[restAssured](https://github.com/odeke-em/restAssured)

      This option is more desirable just in case you want to use the data in real time at any time,

      since it can be updated in real time after extraction from the source.
      

  * Using the options:

   + 1. DirectSQLToJSONLinked.

      For help on commandline options
	  ===================================
		./updateDb.py -h

		Sample usage: 
		+ To get the tracks played by [TheBearRocks](http://thebearrocks.com) every 10 minutes

		  and display the results by most played

		  ./updateDb.py -t 10 

		+ To turn off printing to screen, after every ranking

		  ./updateDb.py -t 10 -d False

		Sample Files: monitor\_start.py and ranks.rk are being included

		monitor\_start.py' is auto-generated and contains the date that is logged

		as the start monitor date

		ranks.rk': Typical file output after crawling

            'http://www.thebearrocks.com/broadcasthistory.aspx, 

           as played on Edmonton radio station 'The Bear Rocks'

		  At the end of every collection period, a \*.tar archive is made containing

	  the ranks in file ranks.rk, the data dump in JSON format, as well

	  as the original sqlite3 database. Also the file with the monitor dates

	  is packaged as well.

  + 2. restAssuredLinked.

	Main file to run is: ./cruncher.py

	Optionally:

	  Provide the url that your restAssured project is accessible at eg:

		./cruncher.py http://129.128.94.85:8000
