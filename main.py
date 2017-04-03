import webapp2
from validate_email import validate_email
class MainHandler(webapp2.RequestHandler):
    def get(self, username = "", password = "", confirm = "", error = "", errorsym2 = "", errorsym1 = "", errorsym0 = ""):
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
                %(error)s
                <form method="post">
                    <table>
                        <tr>
                            <td><p>Username</td>
                            <td><input type="text" name="username" value="%(username)s" required><span class="error">%(errorsym0)s</span></p></td>
                        </tr>
                        <tr>
                            <td><p>Password</td>
                            <td><input type="password" name="password" value="%(password)s" required><span class="error">%(errorsym1)s</span></p></td>
                        </tr>
                        <tr>
                            <td><p>Comfirm Password</p></td>
                            <td><input type="password" name="confirm" value="%(confirm)s" required><span class="error">%(errorsym2)s</span></td>
                        </tr>
                        <tr>
                            <td><p>Email (Optional)</p></td>
                            <td><input type="text" name="email"></td>
                        </tr>
                        <tr>
                            <td><input type="submit"></td>
                        </tr>
                    </table>
                </form>
            </body>
        </html>
        """
        errordict = {"username": username, "password": password, "confirm": confirm, "error": error, "errorsym0": errorsym0, "errorsym1": errorsym1, "errorsym2": errorsym2}
        self.response.write(header % errordict)
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        confirm = self.request.get("confirm")
        email = self.request.get("email")
        if password != confirm or " " in username or (len(email) > 0 and validate_email(email, verify=True)):
            self.get(username, password, confirm, error, email)
        else:
            self.redirect("/welcome?user=" + username)
                    

class Welcome(webapp2.RequestHandler):
    def get(self):
        self.response.write("<h1>Welcome, " + self.request.get("user") + "!</h1>") 
    
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ("/welcome", Welcome)
], debug=True)
