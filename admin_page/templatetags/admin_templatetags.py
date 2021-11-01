from django import template
import datetime, math

register = template.Library()

@register.simple_tag
def get_category_name_by_id(cat_id, categorylist):
    
    
    value_var = ''     
          
    for catlist in categorylist:
        if str(cat_id) == str(catlist.id):
            value_var = catlist.category_name
  
    return value_var 
       

@register.simple_tag
def get_course_name_by_id(course_id, courselist):
    value_var = ''
    
    for cl in courselist:
        if str(course_id) == str(cl.id):
            value_var = cl.course_name
            
    return value_var
    
@register.simple_tag
def get_category_by_course_id(course_id, courselist, categorylist):
    value_var = ''
    
    for cl in courselist:
        for cgl in categorylist:
            if str(cl.id) == str(course_id) and str(cl.category_id) == str(cgl.id):
                value_var = cgl.category_name
                
                    
    return value_var    
    
@register.simple_tag
def get_course_name_by_enrolment_id(enrolment_id, enrolmentlist, courselist):
    value_var = ''
    
    for el in enrolmentlist:        
        for cl in courselist:
            if str(el.id) == str(enrolment_id):
                if str(el.enrolled_course) == str(cl.id):
                    value_var = cl.course_name
            
    return value_var

@register.simple_tag
def get_course_name_by_a_user_id(authentication_user_id, enrolmentlist, courselist):
    value_var = ''
    
    for el in enrolmentlist:        
        for cl in courselist:
            if str(el.user_id) == str(authentication_user_id):
                if str(el.enrolled_course) == str(cl.id):
                    value_var = cl.course_name
            
    return value_var
    
@register.simple_tag
def get_instructor_by_a_user_id(authentication_user_id, enrolment_list, attendance_list, appointment_list, userlist):
    value_var = ''
    
    for apt in appointment_list:
        for ul in userlist:
            for el in enrolment_list:
                for att in attendance_list:
                    if str(el.status) == '1' and str(att.enrolment_id) == str(el.id) and str(el.user_id) == str(authentication_user_id):
                        value_var = ul.lastname +', '+ ul.firstname + ' ' + ul.middlename + ' ' + ul.name_extension 
                
    return value_var
    
@register.simple_tag
def get_schedule_by_a_user_id(authentication_user_id, enrolment_list, attendance_list, appointment_list, schedule_type_list):
    value_var = ''
    
    for apt in appointment_list:       
            for el in enrolment_list:
                for att in attendance_list:
                    for sched in schedule_type_list:
                        if str(sched.id) == str(apt.schedule_type) and str(att.enrolment_id) == str(el.id) and str(el.status) == '1' and str(el.user_id) == str(authentication_user_id):
                            value_var = sched.schedules
                
    return value_var    

@register.simple_tag
def get_schedule_name_by_a_user_id(authentication_user_id, enrolment_list, attendance_list, appointment_list, schedule_type_list):
    value_var = ''
    
    for apt in appointment_list:       
            for el in enrolment_list:
                for att in attendance_list:
                    for sched in schedule_type_list:
                        if str(sched.id) == str(apt.schedule_type) and str(att.enrolment_id) == str(el.id) and str(el.status) == '1' and str(el.user_id) == str(authentication_user_id):
                            value_var = apt.batch_appointment_name
                
    return value_var 
    
@register.simple_tag
def show_appointment_list(instructor_list, schedule_type_list):
    value_var = ''
    
    invisible_string = 'd-none'
    
    instructor_count        = len(instructor_list)
    schedule_type_count     = len(schedule_type_list)
    
    if instructor_count < 1 or schedule_type_count < 1:
        value_var = invisible_string
    else:
        value_var = ''
        
    return value_var
   
@register.simple_tag
def appointment_list_no_display_note(instructor_list, schedule_type_list):
    value_var = ''
    
    instructor_count        = len(instructor_list)
    schedule_type_count     = len(schedule_type_list)
    
    if instructor_count < 1:
        value_var = value_var + 'No instructor records from the database, please add instructor on accounts > instructors in the sidebar \n'
        
    if schedule_type_count < 1:
        value_var = value_var + 'No schedule type records from the database, please add schedule types by clicking the Schedule Types button on the upper right'
    
    string_var = value_var
    
    return string_var

@register.simple_tag
def get_category_type_name(record_list, idval):

    return_var = ''

    for rl in record_list:
        if str(rl.id) == str(idval):
            return_var = rl.category_type_name

    return return_var
    
@register.simple_tag
def get_course_category_by_enrolment_id(authentication_user_id, enrolment_list, courselist, categorylist, cartypelist, categorytypelist):
    value_var = ''
    course_name = ''
    category_name = ''
    course_id = ''
    car_type_id = ''
    category_type_id = ''
    car_type_name = ''
    category_type_name = ''
    
    for cl in courselist:
        for el in enrolment_list:
            if str(cl.id) == str(el.enrolled_course) and str(el.user_id) == str(authentication_user_id):
                course_name = cl.course_name
                course_id = cl.id
                car_type_id = cl.car_type_id
                category_type_id = cl.category_type_id
                
    for cartl in cartypelist:
        if str(cartl.id) == str(car_type_id):
            car_type_name = cartl.car_type_name
            
    for ctl in categorytypelist:
        if ctl.id == category_type_id:
            category_type_name = ctl.category_type_name
                
    for cgl in categorylist:
        for cl in courselist:
            if str(cl.category_id) == str(cgl.id) and str(cl.id) == str(course_id):
                category_name = cgl.category_name
    
    value_var = course_name + '\n(' + category_type_name + ' ' + category_name + ') for ' +car_type_name
    
    return value_var
 

@register.simple_tag
def get_course_details(course_id, courselist):
    value_var = ''  
    
    for cl in courselist:
        if str(cl.id) == str(course_id):
            value_var = str(cl.course_code) + ' | ' + str(cl.course_name) + ' - ' + str(cl.course_description)
                    
    return value_var 
    
@register.simple_tag
def get_course_specialization_details_by_instructor(instructor_user_id, instructor_specialization, courselist):
    value_var = ''
    course_detail = ''
    
    for ispecs in instructor_specialization:
        if str(ispecs.instructor_id) == str(instructor_user_id):
            for cl in courselist:
                if str(cl.id) == str(ispecs.course_id):
                    course_detail = str(cl.course_name) + ' ' + str(cl.course_description)
                    value_var = value_var + course_detail + ' '
                    
    return value_var        

@register.simple_tag
def convert_readable_date(date_here):

    date_here              = str(date_here)
    array_date             = date_here.split('-')
    year                   = int(array_date[0])
    month                  = int(array_date[1])
    day                    = int(array_date[2])

    date_return            = datetime.date(year, month, day)
    
    return date_return
    
@register.simple_tag
def label_status(status):
    return_var = ''
    
    if str(status) == '0':
        return_var = 'Inactive'
    
    if str(status) == '1':
        return_var = 'Active'
        
    return return_var
    
@register.simple_tag
def get_category_name_by_a_user_id(authentication_user_id, enrolmentlist, courselist, categorylist):
    value_var = ''
    
    for el in enrolmentlist:        
        for cl in courselist:
            if str(el.user_id) == str(authentication_user_id):
                if str(el.enrolled_course) == str(cl.id):
                    for catlist in categorylist:
                        if str(catlist.id) == cl.category_id:
                            value_var = catlist.category_name
            
    return value_var
    
@register.simple_tag
def get_car_type(car_type_id, car_type_list):
    value_var = ''
    
    for ctl in car_type_list:
        if str(car_type_id) == str(ctl.id):
            value_var = ctl.car_type_name
            
    return value_var
    
@register.simple_tag
def get_room_details(room_id, rooms_list):
    value_var = ''
    
    for rl in rooms_list:
        if str(rl.id) == str(room_id):
            value_var = rl.room_name + ' | ' + rl.room_no
            
    return value_var
           
@register.simple_tag
def get_username(authentication_user_id, user_list):
    value_var = ''
    
    for ul in user_list:
        if str(authentication_user_id) == str(ul.id):
            value_var = str(ul.username)
            
    return value_var
    
@register.simple_tag
def get_license_type_from_authentication_user_id(authentication_user_id, enrolment_list):
    value_var = ''
    license_type_id = ''
    
    for el in enrolment_list:
        if str(el.user_id) == str(authentication_user_id):
            license_type_id = el.license_type
            
    value_var = license_type_id
    
    if str(license_type_id) == "0":
        value_var = 'None'
        
    if str(license_type_id) == "1":
        value_var = 'Student'

    if str(license_type_id) == "2":
        value_var = 'Non-Professional'
        
    if str(license_type_id) == "3":
        value_var = 'Professional'    
        
    return value_var  

    
       
    
@register.simple_tag
def get_fullname(user_id, userlist):
    value_var = ''
    
    for ul in userlist:
        if str(ul.id) == str(user_id):
            value_var = str(ul.lastname) + ', ' + str(ul.firstname) + ' ' + str(ul.middlename) + ' ' + str(ul.name_extension)
            
    return value_var
    
@register.simple_tag
def get_schedule_type(schedule_id, schedule_type_list):
    value_var = ''
    
    for sched in schedule_type_list:
        if str(schedule_id) == str(sched.id):
            value_var = sched.schedules
            
    return value_var
    
@register.simple_tag
def get_time_schedule_appointment_id(appointment_id, timescheduleappointment):
    value_var = ''
    
    for tsa in timescheduleappointment:
        if str(tsa.appointment_id) == str(appointment_id):
            value_var = str(tsa.id)
            
    return value_var
    
@register.simple_tag
def get_instructor_by_time_schedule_appointment_id(appointment_id, timescheduleappointment, instructor_list):
    value_var = ''
    instructor_id = ''
    
    for tsa in timescheduleappointment:
        if str(tsa.appointment_id) == str(appointment_id):
            instructor_id = str(tsa.instructor_id)
            
    for ins in instructor_list:
        if str(ins.id) == str(instructor_id):
            value_var = ins.firstname + ' ' + ins.middlename + ' ' + ins.lastname + ' ' + ins.name_extension
            
    return value_var

@register.simple_tag
def has_scheduled_days(class_attr_has, class_attr_none, appointment_id, timeschedule_list, appointment_scheduled_day):
    
    value_var = ''
    
    count_record = 0

    for tsl in timeschedule_list:
        if str(appointment_id) == str(tsl.appointment_id) and str(tsl.status) == '1':           
            if str(appointment_scheduled_day) == str(tsl.scheduled_day):
                count_record += 1           
               
    
    if count_record > 0:
        value_var = class_attr_has
    else:
        value_var = class_attr_none
    
    return value_var
   
    
@register.simple_tag
def get_hours_per_day_schedule(schedule_id, schedule_type_list):
    value_var = ''
    
    for sched in schedule_type_list:
        if str(schedule_id) == str(sched.id):
            value_var = sched.hours_per_day
            
    return value_var
    
@register.simple_tag
def get_days_required_from_hours_per_day_schedule(schedule_id, schedule_type_list, course_hours_duration):
    hours_per_day = ''
    
    for sched in schedule_type_list:
        if str(schedule_id) == str(sched.id):
            hours_per_day = sched.hours_per_day            
            
    days_required = int(course_hours_duration) / int(hours_per_day)
    excess_hours = int(course_hours_duration) % int(hours_per_day)
    
    if (excess_hours > 0):
        days_required = int(days_required) + 1
            
    return days_required
    
@register.simple_tag
def get_hours_from_a_user_id(authentication_user_id, enrolment_list, course_list):
    value_var = ''
     
    for el in enrolment_list:
        for cl in course_list:
            if str(cl.id) == str(el.enrolled_course) and str(el.user_id) == str(authentication_user_id):
                    value_var = cl.hours_duration
                    
    return value_var
    
@register.simple_tag
def get_days_duration_from_a_user_id(authentication_user_id, enrolment_list, course_list, schedule_id, schedule_type_list):
    days_duration = 0
    
    course_hours_duration = 0
    hours_per_day = 0
    
    for el in enrolment_list:
        for cl in course_list:
            if str(cl.id) == str(el.enrolled_course) and str(el.user_id) == str(authentication_user_id):
                    course_hours_duration = cl.hours_duration        
                    
    for sched in schedule_type_list:
        if str(schedule_id) == str(sched.id):
            hours_per_day = sched.hours_per_day
            
    excess_duration = int(course_hours_duration) % int(hours_per_day)
   
    
    if excess_duration > 0:
        days_duration = days_duration + 1
    else:
        days_duration = int(course_hours_duration) / int(hours_per_day)
    
    value_var = str(int(days_duration))
            
    return value_var
    
@register.simple_tag
def number_of_enrolled(appointment_id, enrolment_list, appointment_list, attendance_list):

    count_enrolled = 0
    
    for el in enrolment_list:
        for apt in appointment_list:
        
            found = 0
            
            for att in attendance_list:
                if str(att.enrolment_id) == str(el.id):
                
                    found = 1
                    
            if found == 1:
                count_enrolled = count_enrolled + 1
                
    return str(count_enrolled)
    
@register.simple_tag
def get_current_enrolment_id_from_user(authentication_user_id, enrolment_list):
    value_var = ''
    
    for el in enrolment_list:
        if str(el.user_id) == str(authentication_user_id):
            value_var = str(el.id)
    
    return value_var
    
@register.simple_tag
def get_payment_method_by_id(id_value, paymentmethod_list):
    value_var = ''
    
    for list_record in paymentmethod_list:
        if str(id_value) == str(list_record.id):
            value_var = list_record.payment_method
            
    return value_var
   
@register.simple_tag
def is_specialization_assigned_display(class_attr_none, class_attr_has, course_specialization, course_id, instructor_id):
    value_var = ''
    count_record = 0
    
    for cs in course_specialization:
        if str(cs.course_id) == str(course_id) and str(cs.instructor_id) == str(instructor_id):
            count_record = count_record + 1
    
    if count_record > 0:
        value_var = class_attr_has
    else:
        value_var = class_attr_none
        
    return value_var
   
@register.simple_tag
def has_records(class_attr_none, class_attr_has, record_list):
    value_var = ''
    
    count_record = len(record_list)
    
    if count_record > 0:
        value_var = class_attr_has
    else:
        value_var = class_attr_none
        
    return value_var

@register.simple_tag
def has_records_note(note_none, note_has, record_list):
    value_var = ''
    
    count_record = len(record_list)
    
    if count_record > 0:
        value_var = note_has
    else:
        value_var = note_none
        
    return value_var    
    
@register.simple_tag
def reference_number(for_string, digit_limit, sales_transaction_list, enrolment_id, authentication_user_id):
    value_var = ''
    final_value_var = ''
    
    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d")
    
    count_record = 0
    
    count_record = len(sales_transaction_list)
        
    i = count_record + 1    

    string_value = ''
    count_string = len(str(count_record))
        
    zero_count = digit_limit - count_string
    
    for i in range(1, zero_count):
        string_value = string_value + "0"
        
    if zero_count < 0:
        string_value = str(i)
        value_var = string_value
    else:
        value_var = string_value + str(i)
               
        final_value_var = for_string + '-' + datetime_now + '-' + value_var + '-' + str(enrolment_id) + '-' + str(authentication_user_id)  
        
    return final_value_var  

@register.simple_tag
def get_balance_online_payment(authentication_user_id, sales_transaction_list):
    value_var = ''
    
    count_record = 0
    payment_status = '0'
    array_balance = []
    
    for stl in sales_transaction_list:
        if str(stl.user_id) == str(authentication_user_id):
            count_record = count_record + 1
            payment_status = str(stl.status)
            array_balance.append(str(stl.amount_balance))
            
    if count_record > 1:
        if str(payment_status) == '0':
            value_var = array_balance[0]
            
    return value_var           
    
@register.simple_tag
def get_payment_term_id(id_value):
    value_var = ''
    
    if str(id_value) == "1":
        value_var = 'Partial Payment'
    if str(id_value) == "2":
        value_var = 'Full Payment'
            
    return value_var
 
@register.simple_tag
def get_payment_term_status(id_value):
    value_var = ''
    
    if str(id_value) == "1":
        value_var = 'Partially Paid'
    if str(id_value) == "2":
        value_var = 'Fully Paid'
            
    return value_var
    
@register.simple_tag
def get_payment_term_status2(id_value):
    value_var = ''
    
    if str(id_value) == "1":
        value_var = 'Partial Payment'
    if str(id_value) == "2":
        value_var = 'Full Payment'
            
    return value_var
    
@register.simple_tag
def get_payment_term(id_value):
    value_var = ''
    
    if str(id_value) == "1":
        value_var = 'Partial and Full Payment (50% & 100%)'
    if str(id_value) == "2":
        value_var = 'Full Payment (100%)'
            
    return value_var
    
@register.simple_tag
def payment_term_identifier(sales_transaction_list, payment_term):

    # sales_transaction_list and enrolment_list record must be already filtered by applicant's authentication_user_id
    # sales_transaction_list and enrolment_list user_id is the authentication_user_id value of userlist (website_userrecords DB/UserRecord MODEL)
    # SalesTransaction is the Model of sales_transaction_list and Enrolment for enrolment_list
    
    value_var = ''
    
    count_record = len(sales_transaction_list)
    
    if count_record > 0:
        for stl in sales_transaction_list:
            if str(stl.status) == "1" and str(stl.for_payment_term) == "1":
                value_var = '2'
    else:     
        value_var = payment_term
                
    return value_var

@register.simple_tag
def get_payment_term_by_a_user_id(authentication_user_id, enrolment_list):
    value_var = ''
    
    for el in enrolment_list:
        if str(el.user_id) == str(authentication_user_id):
            value_var = get_payment_term(str(el.payment_term))
            
    return value_var
 
@register.simple_tag
def get_payment_method_by_a_user_id(authentication_user_id, sales_transaction_list, paymentmethod_list):
    value_var = ''
    
    for stl in sales_transaction_list:
        if str(stl.user_id) == str(authentication_user_id):
            value_var = get_payment_method_by_id(str(stl.payment_method), paymentmethod_list)
            
    return value_var
    
@register.simple_tag
def hide_if_no_sales_transaction_user(invisible_string, authentication_user_id, sales_transaction_list):
    value_var = ''
    
    count_record = 0
    
    for stl in sales_transaction_list:
        if str(stl.user_id) == str(authentication_user_id):
            count_record = count_record + 1
            
    if count_record < 1:
        value_var = invisible_string       
        
    return value_var
    
@register.simple_tag
def get_category_name_by_course_id(course_id, categorylist, courselist):
    value_var = ''
    
    for cl in courselist:
        if str(cl.id) == str(course_id):
            for catlist in categorylist:
                if str(cl.category_id) == str(catlist.id):
                    value_var = catlist.category_name
            
    return value_var
    
@register.simple_tag
def has_still_payment(enrolment_id, enrolment_list, sales_transaction_list):
    value_var = ''
    count_record = 0
    
    for stl in sales_transaction_list:
        if str(stl.enrolment_id) == str(enrolment_id):
            count_record = count_record + 1
    
    for el in enrolment_list:
        for stl in sales_transaction_list:
            if str(el.id) == str(stl.enrolment_id) and str(el.id) == str(enrolment_id):
                if str(stl.status) == "0":
                    value_var = ''
    
            
    return value_var
    
@register.simple_tag
def payment_term_label_pay_now_modal(payment_term, for_payment_term, partial_payment_standard, sales_transaction_list):
    value_var = ''
    
    count_record = len(sales_transaction_list)
    
    if count_record > 0:
        for stl in sales_transaction_list:
            if str(stl.for_payment_term) ==  "1":
                value_var = 'Payment for Remaining Balance PHP ' + str(stl.amount_balance)
    else:
        if str(payment_term) == "1":
            value_var = 'Partial Payment PHP ' + str(partial_payment_standard)
        if str(payment_term) == "2":
            value_var = "Full Payment"
                
    return value_var
    
@register.simple_tag
def has_enrolment_record(authentication_user_id, enrolment_list):
    value_var = 'd-none'
    
    for el in enrolment_list:
        if str(el.user_id) == str(authentication_user_id):
            value_var = ' '
            
    return value_var
    
@register.simple_tag
def has_enrolment_record_with_display(authentication_user_id, enrolment_list):
    value_var = 'No Enrolment Record or Enrolment Data was delete from the Database'
    
    for el in enrolment_list:
        if str(el.user_id) == str(authentication_user_id):
            value_var = ' '
            
    return value_var    
    
@register.simple_tag
def show_enroll(sales_transaction_list, authentication_user_id):
    value_var = ''
    
    invisible_string = 'd-none'
    
    count_record = 0
    
    for stl in sales_transaction_list:
        if str(authentication_user_id) == str(stl.user_id):
            count_record = count_record + 1
    
    if count_record > 0:
    
        for stl in sales_transaction_list:
          
            if str(stl.user_id) == str(authentication_user_id):
          
                if str(stl.status) == "0" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "1":
                    if count_record == 1:
                        value_var = ''
                    if count_record == 2:
                        value_var = invisible_string 
                        
                if str(stl.status) == "1" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "1":
                
                   value_var = ''
                        
                if str(stl.status) == "0" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "2":
                    if count_record == 1:
                        value_var = invisible_string 
                    if count_record == 2:
                        value_var = ''
                        
                if str(stl.status) == "1" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "2":
                    if count_record == 1:
                        value_var = ''
                    if count_record == 2:
                        value_var = ''
                        
                if str(stl.status) == "1" and str(stl.payment_term) == "2" and str(stl.for_payment_term) == "2":
                    if count_record == 1:
                        value_var = ''
                    
            

    else:
        
        value_var = 'invisible'
               
 
    return value_var  

@register.simple_tag
def get_balance(authentication_user_id, sales_transaction_list):
    value_var = ''
    
    array_value = []
    
    for stl in sales_transaction_list:
        if str(stl.user_id) == str(authentication_user_id):
            array_value.append(str(stl.amount_balance))            
            
    count_record = len(array_value)
    
    if(count_record > 0):    
        amount_balance = array_value[count_record - 1]
        value_var = amount_balance
    
    return value_var
    
@register.simple_tag
def show_declare_payment_cash(false_string, true_string, authentication_user_id, enrolment_list, sales_transaction_list):
    value_var = ''
    
    count_record = 0
    
    for el in enrolment_list:
        if str(el.user_id) == str(authentication_user_id):
            if str(el.payment_method) != "3":
                value_var = true_string

    for stl in sales_transaction_list:
        if str(stl.user_id) == str(authentication_user_id) and str(stl.payment_method) == "3" and str(stl.status) == "1" and str(stl.payment_term) == "2":
            count_record = count_record + 1            
            
    if count_record > 0:
        value_var = true_string
        
               
    return value_var
    
@register.simple_tag
def invisible_if_partially_paid_cash(true_string, false_string, authentication_user_id, sales_transaction_list):
    value_var = ''

    found = 0

    for stl in sales_transaction_list:
        if str(stl.user_id) == str(authentication_user_id) and str(stl.payment_method) == "3" and str(stl.status == '1') and str(stl.for_payment_term) == '1':
           found = 1

    if found == 1:
        value_var = true_string
    else:
        value_var = false_string


    return value_var
    
@register.simple_tag
def show_declare_payment(sales_transaction_list, authentication_user_id):
    value_var = ''
    
    count_record = 0
    
    for stl in sales_transaction_list:
        if str(authentication_user_id) == str(stl.user_id):
            count_record = count_record + 1
    
    if count_record > 0:
    
        for stl in sales_transaction_list:
          
            if str(stl.status) == "0" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "1":
                if count_record == 1:
                    value_var = 'invisible'
                if count_record == 2:
                    value_var = ''
                    
            if str(stl.status) == "1" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "1":
                if count_record == 1:
                    value_var = ''
                if count_record == 2:
                    value_var = ''
                    
            if str(stl.status) == "0" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "2":
                if count_record == 1:
                    value_var = ''
                if count_record == 2:
                    value_var = 'invisible'
                    
            if str(stl.status) == "1" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "2":
                if count_record == 1:
                    value_var = ''
                if count_record == 2:
                    value_var = 'invisible'
                    
            if str(stl.status) == "1" and str(stl.payment_term) == "2" and str(stl.for_payment_term) == "2":
                if count_record == 1:
                    value_var = 'invisible' 
               

    else:
        
        value_var = 'invisible'
               
 
    return value_var  
    
@register.simple_tag
def show_pay_now(sales_transaction_list):
    value_var = ''
    
    count_record = len(sales_transaction_list)
    
    invisible_string = 'd-none'
    
    if count_record > 0:
    
        for stl in sales_transaction_list:
          
            if str(stl.status) == "0" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "1":
                if count_record == 1:
                    value_var = invisible_string
                if count_record == 2:
                    value_var = ''
                    
            if str(stl.status) == "1" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "1":
                if count_record == 1:
                    value_var = ''
                if count_record == 2:
                    value_var = ''
                    
            if str(stl.status) == "0" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "2":
                if count_record == 1:
                    value_var = ''
                if count_record == 2:
                    value_var = invisible_string
                    
            if str(stl.status) == "1" and str(stl.payment_term) == "1" and str(stl.for_payment_term) == "2":
                if count_record == 1:
                    value_var = ''
                if count_record == 2:
                    value_var = invisible_string
                    
            if str(stl.status) == "1" and str(stl.payment_term) == "2" and str(stl.for_payment_term) == "2":
                if count_record == 1:
                    value_var = invisible_string   

            if str(stl.status) == "0" and str(stl.payment_term) == "2" and str(stl.for_payment_term) == "2":
                if count_record == 1:
                    value_var = invisible_string
 
    return value_var   


@register.simple_tag
def get_age(birthdate):

    array_bdate             = birthdate.split('-')
    year                    = int(array_bdate[0])
    month                   = int(array_bdate[1])
    day                     = int(array_bdate[2])
    
    month_now               = int(datetime.datetime.now().strftime('%m'))
    day_now                 = int(datetime.datetime.now().strftime('%d'))

    date_diff               = datetime.date.today() - datetime.date(year, month, day)
    age                     = date_diff.total_seconds() / 60 / 60 / 24 / 365

    if(month_now >= month):
        if(month_now == month):
            if(day_now >= day):

                age = math.ceil(age)
                
            else:

                age = math.floor(age)
            
        else:

            age = math.ceil(age)

    else: 

        age = math.floor(age)
        
    return age
    
@register.simple_tag
def if_enrolled_student(authentication_user_id, user_list):
 
    return_value = '0'
    count_record = 0
    
    for ul in user_list:
        if str(ul.authentication_user_id) == str(authentication_user_id) and str(ul.role_id) == '2':
            count_record = count_record + 1
            
    if count_record > 0:
        return_value = '1'
    else:
        return_value = '0'
        
    return return_value

@register.simple_tag
def average_student_age(user_list):

    sum_age = 0
    sl_age = 0
    count_record = len(user_list)
    
    for sl in user_list:      
        birthdate = sl.birthdate
        sl_age = get_age(birthdate)
        sum_age = sum_age + sl_age      
    
    if count_record < 1 or sum_age < 1:
        average_age = 0
    else:    
        average_age = sum_age / count_record
    
    return str(average_age)
    
@register.simple_tag
def ave_no_of_students_per_course(courselist,enrolment_list, user_list):

    no_students = 0
    course_taken_count = 0
    average_no_student = 0
    
    for cl in courselist:
        for el in enrolment_list:
            authentication_user_id = str(el.user_id)
            if str(cl.id) == str(el.enrolled_course) and if_enrolled_student(authentication_user_id, user_list) == '1':
                course_taken_count = course_taken_count + 1
                
    no_students = len(enrolment_list)

    if no_students < 1 or course_taken_count < 1:
        average_no_student = 0
    else:
        average_no_student = no_students / course_taken_count
        
    return average_no_student
            
   