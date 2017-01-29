#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

class MainHandler(webapp2.RequestHandler):
    def buildSection(self,title,value,fillIn):
        return ("""
                <tr>
                    <td><label for="%s">%s</label></td>
                    <td>
                        <input type="text" name="%s" value = %s>
                    </td>
                </tr>
                """ %(value,title,value,fillIn))
    
    def buildForm(self,what,usrnm,pswrd1,pswrd2,email):
        header =  "<h3>Sign Up</h3>"
        beginForm = '<form action="/" method="post"> <table>'
        usrForm = self.buildSection("Username","username",usrnm)
        pswrd1Form = self.buildSection("Password","password1",pswrd1)
        pswrd2Form = self.buildSection("Confirm Password","password2",pswrd2)
        emailForm = self.buildSection("Email (optional)","email",email)
        endForm = '</table><input type="submit" value="Add It"/></form>'
        return(header+beginForm+usrForm+pswrd1Form+pswrd2Form+emailForm+endForm)
                
    def get(self):
        self.response.write(self.buildForm(self,'','','',''))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
