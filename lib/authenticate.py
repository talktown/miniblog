from lib import setting_service


def login_with_email(request):
    email = request.form['email']
    password = request.form['password']
    return email == setting_service.get("admin_email") and password == setting_service.get("admin_password")
