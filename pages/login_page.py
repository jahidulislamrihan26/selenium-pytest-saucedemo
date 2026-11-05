from .base_page import BasePage


class LoginPage(BasePage):
    path = "/"
    USERNAME = BasePage.dt("username")
    PASSWORD = BasePage.dt("password")
    SUBMIT = BasePage.dt("login-button")
    ERROR = BasePage.dt("error")

    def sign_in(self, username: str, password: str) -> None:
        if username:
            self.type_into(self.USERNAME, username)
        if password:
            self.type_into(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def error_text(self) -> str:
        return self.text_of(self.ERROR)

    def password_is_masked(self) -> bool:
        return self.find(self.PASSWORD).get_attribute("type") == "password"

    def is_shown(self) -> bool:
        return self.is_present(self.SUBMIT)
