import ephem
from twitter import *
from datetime import datetime, date
import time
import sqlite3

def TimeZoneDictionary(time_zone, hours):
    time = {'America/Chicago': -6,
            'US/Mountain': -7,
            'US/Arizona': -8,
            'America/New_York':-5,
            'US/Eastern': -5,
            'US/Central': -6,
            'America/Indianapolis': -5,
            'Pacific/Samoa': 13,
            'US/Pacific': -8,
            'America/Denver': -7,
            'America/Puerto_Rico': -4,
            'America/Los_Angeles': -8,
            'Pacific/Guam': 10,
            'America/Adak': -9,
            'America/Virgin': -4,
            'Pacific/Saipan': 10,
            'US/Alaska': -9,
            'US/Hawaii': -10,
    }

    calculated = hours + time[time_zone]
    if(calculated < 0):
        return 24 + calculated 
    elif (calculated > 24):
        return calculated - 24
    else:
        return calculated

def stringConverter(time_zone, time_string):
    year_month_day = time_string[0:10]
    minute_second = time_string[12:]
    hour = time_string[10] + time_string[11]
    hour = int(hour)
    conHour = TimeZoneDictionary(time_zone, hour)
    conHour = str(conHour)
    new_time = conHour + minute_second

    return new_time


def main():
    #Acquire personal twitter API for key/secret
    # https://apps.twitter.com/
    CON_KEY = 'placeholder'
    CON_SECRET = 'placeholder'
    ACC_KEY = 'placeholder'
    ACC_SECRET = 'placeholder'

    t = Twitter(auth=OAuth(ACC_KEY, ACC_SECRET, CON_KEY, CON_SECRET))

    DataBase = sqlite3.connect('us_only.sq3')
    c = DataBase.cursor()
    sun = ephem.Sun()
    city = input("City: ")
    state = input("State: ")
    region = 'US/' + state

    c.execute('select latitude, longitude, time_zone from sol_places where name = "{}" and region = "{}"'.format(city, region))    
    
    for i in c:
        latitude = i[0]
        longitude = i[1]
        timeZone = i[2]

    loc = ephem.Observer()
    loc.lat = str(latitude)
    loc.lon = str(longitude)
    sun.compute(loc)

    sunrise = str(loc.previous_rising(sun))
    sunset = str(loc.next_setting(sun))

    loc.horizon = '-6'
    dawn = str(loc.previous_rising(sun, use_center=True))
    dusk = str(loc.next_setting(sun, use_center=True))

    local_sunrise = stringConverter(timeZone, sunrise)
    local_sunset = stringConverter(timeZone, sunset)
    local_dawn = stringConverter(timeZone, dawn)
    local_dusk = stringConverter(timeZone, dusk)
    
    t.statuses.update(status='In {}, {} dawn began at {}, the sun rose at {}, the sun will set at {}, and dusk will be at {}.'.format(city, state, local_dawn, local_sunrise, local_sunset, local_dusk))

    
if __name__ == '__main__':
    main()

 '''Copyright (C) 2014  Andrew Ross

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

