import webapp2
import cgi
import re
def valid_username(username):
    user_re = re.compile("^[a-zA-Z0-9]{3,20}$")
    return user_re.search(username)

class MainHandler(webapp2.RequestHandler):

    def get(self, username = "", password = "", confirm = "", email = ""):
        header = """
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    .error {
                        color: red;
                    }
                </style>
            </head>
            <body>
                <h1>Signup</h1>
                <form method="post">
                    <table>
                        <tr>
                            <td><p>Username</td>
                            <td><input type="text" name="username" value="%(username)s" required><span class="error">%(errorsym0)s</span></p></td>
                        </tr>
                        <tr>
                            <td><p>Password</td>
                            <td><input type="password" name="password" required><span class="error">%(errorsym1)s</span></p></td>
                        </tr>
                        <tr>
                            <td><p>Confirm Password</p></td>
                            <td><input type="password" name="confirm" required><span class="error">%(errorsym2)s</span></td>
                        </tr>
                        <tr>
                            <td><p>Email (Optional)</p></td>
                            <td><input type="email" name="email" value="%(email)s"><span class="error">%(errorsym3)s</span></td>
                        </tr>
                        <tr>
                            <td><input type="submit"></td>
                        </tr>
                    </table>
                </form>
            </body>
        </html>
        """

        errordict = {"username": username, "email": email, "errorsym0": "", "errorsym1": "", "errorsym2": "", "errorsym3": ""}

        if valid_username(username) == None and len(username) > 0:
            errordict["errorsym0"] = "That's an invalid username."
        if password != confirm:
            errordict["errorsym2"] = "Passwords don't match."
            
        self.response.write(header % errordict)
        
    def post(self):
        username = cgi.escape(self.request.get("username"))
        password = self.request.get("password")
        confirm = self.request.get("confirm")
        email = cgi.escape(self.request.get("email"))

        if password != confirm or valid_username(username) == None:
            self.get(username, password, confirm, email)
        else:
            self.redirect("/welcome?user=" + username)

class Welcome(webapp2.RequestHandler):
    
    def get(self):
        self.response.write("<h1>Welcome, " + self.request.get("user") + "!</h1>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ("/welcome", Welcome)
], debug=True)
