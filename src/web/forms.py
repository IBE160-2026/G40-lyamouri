"""Forms (AD-10)."""

from django import forms


class LoginForm(forms.Form):
    """The customer number and password of Innlogging (FR-1).

    A blank field, or a NUL character that the database cannot store, is as wrong
    as a wrong password: the view shows one message for all of them.
    """

    customer_number = forms.CharField()
    password = forms.CharField(strip=False)
