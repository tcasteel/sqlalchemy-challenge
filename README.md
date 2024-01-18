# sqlalchemy-challenge

Within this challenge we were tasked to take two of the data sets that we were given and come up with two tables one for the temperatures and one for the precipitation.

After setting up my engine and my session, I was able to get the first set of data ran through for the precipitation through a 12 month time span.
With using the lastest date on the data sheet for the precipitation and then from that date finding that date going back a year with using latest_date - dt.timedelta(days=365) to be able to grab the date back a year.
After setting the start and end dates for the for the data, with having a start and end date we are able to set the inbetween to be able to split it up in the 12 months that is being asked of.
after setting the 12 months and setting the intervals for the bar plot, we are able to set the plot up to have the data that is being asked of.
with setting a range and the step size we are able to gather the dates sporadically without over crowding the x axis.
Before the plot is shown, it is saved in the static folder to be used within flask later.

Then using the same data we chart the summary with using describe for the 'prcp' data.

Using a for loop we are able to gather all the times that each station pops up in the data.
within the code to get that count we create a section for most active stations using a query to be able to measure each of the unique stations and count each time they show up.

With using the most active station code we are able to find the temp stats with using func.min,max,avg to be able to gather the max min and avg for the most active station.

Again with using the most active station code, we are able to find the over all 12 month temp observations.
Within the graph we are able to find the freqeuncy of the amount of times that at temp shows up within the data set.

Then close the session.

After all that has been written, started on the flask code.

On the App.py file imported flask and Datetime, for datetime, timedelta

Added all of the flask requirements, added the path for static so that the saved pictures would be able to be displayed on the front page of the site that is being created.
After the base and engine have been created, along with the measurement, station, and session parameters.
Created each of the routes along with Jsonify with them to be able to provide each link with the information that is being asked of.
When it comes to the start/end portion, it grabs the entire data sheet to be able to grab the min max and avg of what ever date that you are looking for that is within the data set.
When adding the end portion it grabs the average of the two dates to be able to give a proper answer to the ask.

With the home page, there is an Index.html portion to be able to show the images on the home page of the site that is being written.

After all of that there is a 
if __name__ == "__name__"
  app.run(debug=True)
So that the site can complete its full steps.
