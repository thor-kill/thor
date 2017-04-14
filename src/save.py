"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.
"""

author = ["Thorkill"]
version = "0.1"

from json import dumps

def save_json(profile, output):
	if output[-1] != '/':
		output += '/'
	if profile != None:
		data = dumps(profile)
		name = profile[3]
		if isinstance(name, tuple): name = name[0]
		name = "%s_%s-%s-%s-%s" %(name, profile[0].tm_year, profile[0].tm_mon, profile[0].tm_mday, profile[0].tm_hour)
		with open(output + name, 'w') as page:
			page.write(data)
