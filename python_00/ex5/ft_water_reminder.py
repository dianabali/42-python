def ft_water_reminder():
    days_since = int(input("Days since last watering: "))
    if days_since > 2:
        print("Water the plants!")
    else:
        print("Plants are fine")


ft_water_reminder()
