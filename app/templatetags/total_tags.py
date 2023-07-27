from django import template


register = template.Library()

@register.filter
def total_value(loadPurchase):
    sum1=sum(float(object.get('amount', 0)) for object in loadPurchase)
    rounded_num = round(sum1, 2)

    return rounded_num 

@register.filter
def total_fuel(fillManualArray):

    return sum(float(object.get('totalFilled', 0.0)) for object in fillManualArray)


@register.filter
def total_fuel_amout(fillManualArray):
    total=0
    for i in fillManualArray:
        total+=float(i.get('amountPerLitre'))*float(i.get('totalFilled'))
    return total

    
@register.filter
def multiply(value1, value2):

    v = float(value1) * float(value2)

    ro = round(v, 1)
    return ro 


@register.filter
def total_auto_filled(Auto_Fill_Report):

    value = sum(float(object.get('volume', 0)) for object in Auto_Fill_Report)/1000
    
    ro = round(value, 1)
    return ro 
    
@register.filter
def total_manul_filled(Auto_Fill_Report):

    return sum(float(object.get('totalFilled', 0)) for object in Auto_Fill_Report)



@register.filter
def checkgen(value1, value2):
    for i in value1:
        if i == value2:
            return i


    return 0


@register.filter
def lasts(fillManualArray):
    volume=0.0
    for i in fillManualArray:
        if i == fillManualArray[0]:
            volume = float(i['totalFilled'])

  
    return volume


@register.filter
def amt(fillManualArray):
    amt=0.0
    for i in fillManualArray:
        if i == fillManualArray[0]:
            amt = float(i['amountPerLitre'])

  
    return amt

@register.filter
def running1lt(timeDiffrenceSum):
    if timeDiffrenceSum != "0":
    
        hr1=int(timeDiffrenceSum)/3600

        rounded_num = round(hr1, 2)
    
        return rounded_num
    return 0.00    


@register.filter
def running1hr(timeDiffrenceSum):

    if timeDiffrenceSum != "0":
    
        hr1=int(timeDiffrenceSum)/3600

        rounded_num = round(hr1, 2)

        h2=1/rounded_num
        h2=round(h2, 5)
        return h2
    return 0.00    
  
    
@register.filter
def mon(monthlist):
    months_quoted = ", ".join([f"'{month}'" for month in monthlist])

    return months_quoted



@register.filter
def rou(value):
    
    ro=round(value,1)
    return ro



@register.filter
def volume(value):
    
    v = int(value)/1000

    ro=round(v,1)

    return ro


@register.filter
def total_filled(value):

    value = sum(float(object.get('totalFilled', 0)) for object in value)
    
    ro = round(value, 1)
    return ro 