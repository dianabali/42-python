def ft_count_days(day, total):
    if day > total:
        print("Harvest time!")
        return
    print("Day ", day)
    ft_count_days(day + 1, total)


def ft_count_harvest_recursive():
    days_until = int(input("Days until harvest: "))
    ft_count_days(1, days_until)


ft_count_harvest_recursive()
