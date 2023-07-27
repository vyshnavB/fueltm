from django.urls import path
from . import views


urlpatterns = [

        path('',views.Login,name='Login'),

        path('Logout',views.Logout,name='Logout'),

        path('Register',views.Register,name='Register'),

        path('Signup',views.Signup,name='Signup'),

        path('Home',views.Home,name='Home'),

        path('Add_Application',views.Add_Application,name='Add_Application'),

        

        path('Users',views.Users,name='Users'),

        path('Hotspot',views.Hotspot,name='Hotspot'),

        path('Notification_Delay',views.Notification_Delay,name='Notification_Delay'),

        path('Add_Users',views.Add_Users,name='Add_Users'),

        path('Add_Device',views.Add_Device,name='Add_Device'),

        path('Power_Manager',views.Power_Manager,name='Power_Manager'),

        path('Fill_Fuel',views.Fill_Fuel,name='Fill_Fuel'),

        path('Purchase',views.Purchase,name='Purchase'),

        path('Add_New_Purchase',views.Add_New_Purchase,name='Add_New_Purchase'),

        path('Service',views.Service,name='Service'),

        path('Add_New_Service',views.Add_New_Service,name='Add_New_Service'),
        
        path('Reports',views.Reports,name='Reports'),


        path('Verifications',views.Verifications,name='Verifications'),

        path('otpgenerate',views.otpgenerate,name='otpgenerate'),

        path('OTP',views.OTP,name='OTP'),

        path('Verify',views.Verify,name='Verify'),

        path('Edit_Device',views.Edit_Device,name='Edit_Device'),

        path('Edit_Application',views.Edit_Application,name='Edit_Application'),

        path('Edit_Purchase/<int:id>',views.Edit_Purchase,name='Edit_Purchase'),

        path('Fill_Tank_Details',views.Fill_Tank_Details,name='Fill_Tank_Details'),

        path('Edit_Fill_Fuel/<int:id>',views.Edit_Fill_Fuel,name='Edit_Fill_Fuel'),

        path('Edit_Service/<int:id>',views.Edit_Service,name='Edit_Service'),

        path('Edit_Users/<str:id>',views.Edit_Users,name='Edit_Users'),

        path('Update_Status/<str:id>',views.Update_Status,name='Update_Status'),

        path('Automatic_mode',views.Automatic_mode,name='Automatic_mode'),

        path('Manul_mode',views.Manul_mode,name='Manul_mode'),

        path('alertmessage',views.alertmessage,name='alertmessage'),

        path('alertmessage1',views.alertmessage1,name='alertmessage1'),

        path('Gen_on',views.Gen_on,name='Gen_on'),

        path('Gen_off',views.Gen_off,name='Gen_off'),

        path('Load_on_dg',views.Load_on_dg,name='Load_on_dg'),

        path('Load_on_eb',views.Load_on_eb,name='Load_on_eb'),



        path('link_callback',views.link_callback,name='link_callback'),

        path('Auto_report',views.Auto_report,name='Auto_report'),


        path('Manul_report',views.Manul_report,name='Manul_report'),

        path('Purchase_report',views.Purchase_report,name='Purchase_report'),

        path('Service_report',views.Service_report,name='Service_report'),


        path('google_login',views.google_login,name='google_login'),

        path('Reset_Password',views.Reset_Password,name='Reset_Password'),

        path('Otp_Password',views.Otp_Password,name='Otp_Password'),

        path('New_Password',views.New_Password,name='New_Password'),

        path('get_rating_kw',views.get_rating_kw,name='get_rating_kw'),

        path('Emergency_Stop',views.Emergency_Stop,name='Emergency_Stop'),

        path('Restart',views.Restart,name='Restart'),

        path('contact',views.contact,name='contact'),

        

        


        

        

      


        

        

        


        





        



        



        

        
        
     




        


        


        


        


        


        

        


        


        


        


       


        


        

]