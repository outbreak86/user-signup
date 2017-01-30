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
import re
import cgi
class MainHandler(webapp2.RequestHandler):
    #Used for regular expression
    #Check the input of fields
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PSWRD_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"[\S]+@[\S]+.[\S]+$")
    #Used to hold error messages
    userror = ''
    ps1error = ''
    ps2error = ''
    emerror = ''

     def valid_username(self,username):
         if(USER_RE.match(username)):
             self.userror = 'Invalid Username'
             return False
         else:
             self.userror = ''
             return True

    def valid_pswrd(self,pswrd1):
        if(PSWRD_RE.match):
            self.ps1error = 'Invalid Password'
            return false
        else:
            self.ps1error = ''
            return true

    def valid_email(self,email):
         if(EMAIL_RE.match(email)):
             self.emerror= 'Invalid email'
             return False
         else:
             self.emerror = ''
             return True

    #Build the sections of the table and inputs
    def buildSection(self,title,value,fillIn,error):
        return ("""
                <tr>
                    <td><label for="%s">%s</label></td>
                    <td>
                        <input type="text" name="%s" value = %s>
                        <span class="error">%d</span>
                    </td>
                </tr>
                """ %(value,title,value,fillIn,error))
    #Used to build the over all table
    def buildForm(self,what,usrnm,pswrd1,pswrd2,email):
        header =  "<h3>Sign Up</h3>"
        beginForm = '<form action="/" method="post"> <table>'
        usrForm = self.buildSection("Username","username",usrnm,self.userror)
        pswrd1Form = self.buildSection("Password","password1",pswrd1,self.ps1error)
        pswrd2Form = self.buildSection("Confirm Password","password2",pswrd2,self.ps2error)
        emailForm = self.buildSection("Email (optional)","email",email,self.emerror)
        endForm = '</table><input type="submit" value="Add It"/></form>'
        return(header+beginForm+usrForm+pswrd1Form+pswrd2Form+emailForm+endForm)

    def get(self):
        self.response.write(self.buildForm(self,'','','',''))

    def post(self):
        
        no_error = True
        
        username = self.request.get('username')
        password = self.request.get('password1')
        password2 = self.request.get('password2')
        email = self.request.get('email')

        if(!valid_username(self,username)):
            no_error = False
            
        if(!valid_pswrd(self,password1)):
            no_error = False
            
        if(!valid_email(self,email)):
            no_error = False
            
        if(password1 != password):
            ps2error = 'Passwords do not match'
            no_error = False
        else:
            ps2error = ''

        
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
