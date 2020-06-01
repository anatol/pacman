#  Copyright (c) 2020 Pacman Development Team <pacman-dev@archlinux.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import http
import http.server
import sys

class pmHTTPServer(http.server.ThreadingHTTPServer):
    pass

class pmHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """BaseHTTPRequestHandler subclass with helper methods and common setup"""

    logfile = sys.stderr

    def respond_bytes(self, response, ctype="application/octet-stream", headers={}):
        self.protocol_version = "HTTP/1.1"
        self.send_response(http.HTTPStatus.OK)
        for header, value in headers.items():
            self.send_header(header, value)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def respond_string(self, response, headers={}):
        self.respond_bytes(response.encode('UTF-8'), 'text/plain; charset=utf-8', headers)

    def log_message(self, format, *args):
        if callable(self.logfile):
            self.logfile = self.logfile()
        self.logfile.write("%s - - [%s] %s\n" %
                (self.address_string(),
                self.log_date_time_string(),
                format%args))

class pmStringHTTPRequestHandler(pmHTTPRequestHandler):
    """pmHTTPRequestHandler subclass to respond with simple string messages"""

    responses = dict()

    def do_GET(self):
        if self.path in self.responses:
            response = self.responses[self.path]
            if isinstance(response, dict):
                self.respond_string(response.get('body', ''),
                        response.get('headers', []))
            else:
                self.respond_string(response)
        else:
            self.send_error(http.HTTPStatus.NOT_FOUND);
