from handy.accountDetails import AccountDetail
from handy.useful_functions import grab_username_from_email
from pages.stark import Stark

not_okay = True
email_id=""
while not_okay:
    email_id = input("Enter your email-ID only gmail : ")
    if email_id.split('@')[1] == 'gmail.com':
        print("Thank you!")
        not_okay = False
username = grab_username_from_email(email_id)
accountdetail = AccountDetail(get_state="ohio")
student_info = accountdetail.get_student_info()
print(student_info)
stark = Stark(username, student_info)
stark.start_process()
