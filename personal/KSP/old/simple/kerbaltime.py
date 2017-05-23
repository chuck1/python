


class KerbalTime:
	hoursPerDay = 6;
	daysPerYear = 426;

	def __init__(self, t):
		self.t = t

	def setDateFormat(self, hoursPerDay, daysPerYear):
		self.hoursPerDay = hoursPerDay
		self.daysPerYear = daysPerYear
		#return $(this).trigger('dateFormatChanged');

	def secondsPerDay(self):
		return this.hoursPerDay * 3600;
	
	def hms(self):
		hours = (self.t / 3600) | 0;
		t = self.t % 3600;
		mins = (t / 60) | 0;
		secs = t % 60;
		return [hours, mins, secs];
	
	def ydhms(self):
		_ref = self.hms()
		hours = _ref[0]
		mins = _ref[1]
		secs = _ref[2]

		days = (hours / KerbalTime.hoursPerDay) | 0
		hours = hours % KerbalTime.hoursPerDay
		years = (days / KerbalTime.daysPerYear) | 0
		days = days % KerbalTime.daysPerYear
		return [years, days, hours, mins, secs]

	def __add__(self, t):
		return KerbalTime(self.t + t.t)

def hmsString(hour, min, sec):
	if (min < 10):
		min = "0" + min
		
	if (sec < 10):
		sec = "0" + sec
		
	return "" + hour + ":" + min + ":" + sec

def fromDuration(years = 0, days = 0, hours = 0, mins = 0, secs = 0):
	if (years == None):
		years = 0
		
	if (days == None):
		days = 0
		
	if (hours == None):
		hours = 0
		
	if (mins == None):
		mins = 0
		
	if (secs == None):
		secs = 0
		
	return KerbalTime(((((+years * KerbalTime.daysPerYear) + +days) * KerbalTime.hoursPerDay + +hours) * 60 + +mins) * 60 + +secs)
	
def fromDate(year, day, hour, min, sec):
	if (year == null):
		year = 0;
		
	if (day == null):
		day = 0;
		
	if (hour == null):
		hour = 0;
		
	if (min == null):
		min = 0;
		
	if (sec == null):
		sec = 0;
		
	return this.fromDuration(+year - 1, +day - 1, +hour, +min, +sec);

#def parse(dateString):
#	components = dateString.match("(\d+)\/(\d+)\s+(\d+):(\d+):(\d+)");
#	components.shift();
#	return this.fromDate.apply(this, components);
	


