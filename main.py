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
import logging
class MainHandler(webapp2.RequestHandler):
    #Used for regular expression
    #Check the input of fields
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PSWRD_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"[\S]+@[\S]+.[\S]+$")
    #Used to hold error messages
    userror = 'Invalid Username'
    ps1error = 'Invalid Password'
    ps2error = 'Passwords do not match'
    emerror = 'Invalid email'

    def valid_username(self,username):
         if(self.USER_RE.match(username)):
             return False
         else:
             return True

    def valid_pswrd(self,pswrd1):
        if(self.PSWRD_RE.match(pswrd1)):
            return False
        else:
            return True

    def valid_email(self,email):
         if(self.EMAIL_RE.match(email)):
             return False
         else:
             return True

    #Build the sections of the table and inputs
    def buildSection(self,title,value,fillIn,error):
        return ("""
                <tr>
                    <td><label for="%s">%s</label></td>
                    <td>
                        <input type="text" name="%s" value = %s>
                        <span class="error">%s</span>
                    </td>
                </tr>
                """ %(value,title,value,fillIn,error))

    def buildPassword(self,title,value,fillIn,error):
        return ("""
                <tr>
                    <td><label for="%s">%s</label></td>
                    <td>
                        <input type="password" name="%s" value = %s>
                        <span class="error">%s</span>
                    </td>
                </tr>
                """ %(value,title,value,fillIn,error))
    #Used to build the over all table
    def buildForm(self,usrnm,email,usb,ps1b,ps2b,emb):
        header =  """
    <html>
        <head>
            <style>
                  .error {
                        color: red;
                    }
            </style>
        </head>
        <body>
            <h3>Sign Up</h3>
                    """
        beginForm = '<form action="/" method="post"> <table>'
        if(usb):
            usrForm = self.buildSection("Username","username",usrnm,self.userror)
        else:
            usrForm = self.buildSection("Username","username",usrnm,'')
            
        if(ps1b):
            pswrd1Form = self.buildPassword("Password","password1","",self.ps1error)
        else:
            pswrd1Form = self.buildPassword("Password","password1","",'')
            
        if(ps2b):
            pswrd2Form = self.buildPassword("Confirm Password","password2","",self.ps2error)
        else:
            pswrd2Form = self.buildPassword("Confirm Password","password2","",'')
            
        if(emb):
            emailForm = self.buildSection("Email (optional)","email",email,self.emerror)
        else:
            emailForm = self.buildSection("Email (optional)","email",email,'')
        
        endForm = """
                </table><input type="submit" value="Add It"/>
            </form>
        </body>
    </html>
        """
        return(header+beginForm+usrForm+pswrd1Form+pswrd2Form+emailForm+endForm)

    def get(self):
        username = self.request.get('username')
        email = self.request.get('email')
        usb = (self.request.get('usbool')=='1')
        ps1b = (self.request.get('ps1bool')=='1')
        ps2b = (self.request.get('ps2bool')=='1')
        emb = (self.request.get('embool')=='1')
        self.response.write(self.buildForm(username,email,usb,ps1b,ps2b,emb))

    def post(self):
        
        no_error = True
        errorList = '?'
        username = self.request.get('username')
        password1 = self.request.get('password1')
        password2 = self.request.get('password2')
        email = self.request.get('email')

        if(self.valid_username(username)):
            errorList = errorList+'usbool=1&'
            no_error = False
        else:
            errorList = errorList+'username=%s&'%(cgi.escape(username))
        if(self.valid_pswrd(password1)):
            errorList = errorList+'ps1bool=1&'
            no_error = False

        if(email != ''):
            if(self.valid_email(email)):
                errorList = errorList+'embool=1&'
                no_error = False
            else:
                errorList = errorList+'email=%s&'%(cgi.escape(email))
            
        if(password2 != password1):
            errorList = errorList+'ps2bool=1'
            no_error = False

        if(no_error == False):
             self.redirect('/'+errorList)
        else:
             self.redirect('/welcome?us=%s'%(cgi.escape(username)))

class WelHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('us')
        self.response.write("<h3>Welcome %s</h3>"%(username))
             
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelHandler)
], debug=True)
