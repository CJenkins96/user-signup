import webapp2
import cgi
import re
def valid_username(username):
    user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return user_re.match(username)
def valid_password(password):
    password_re = re.compile(r"^.{3,20}$")
    return password_re.match(password)
def valid_email(email):
    email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return email_re.match(email)
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
                %(error)s
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
                            <td><p>Comfirm Password</p></td>
                            <td><input type="password" name="confirm" required><span class="error">%(errorsym2)s</span></td>
                        </tr>
                        <tr>
                            <td><p>Email (Optional)</p></td>
                            <td><input type="email" name="email" value="%(email)S"><span class="error">%(errorsym3)s</span></td>
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
        if valid_username(username):
            errordict["errorsym0"] = "That's an invalid username."
        if valid_password(password):
            errordict["errorsym1"] = "That's an invalid password."
        if password != confirm:
            errordict["errorsym2"] = "Passwords don't match."
        if valid_email(email):
            errordict["errorsym3"] = "That's an invalid email."
        self.response.write(header % errordict)
    def post(self):
        username = cgi.escape(self.request.get("username"))
        password = self.request.get("password")
        confirm = self.request.get("confirm")
        email = cgi.escape(self.request.get("email"))
        if password != confirm or valid_username(username) or valid_password(password) or (len(email) > 0 and valid_email(email)):
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
