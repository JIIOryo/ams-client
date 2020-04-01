import datetime

def formated_str_now_date():
    return datetime.datetime.now().strftime('%m/%d %H:%M')

def least_squares(data):
    """
    Parameters
    ----------
    data : list[list]
        list of { list of raw sensor value and theoretical value }
        e.g. 
        data = [
            [740, 23],
            [750, 23.2],
            [760, 23.34],
            ...
        ]

    Returns
    ----------
    int
        a
    int
        b
        [expected value] = a * [raw sensor value] + b
    """
    sum_xy = sum_x = sum_y = sum_x2 = 0
    N = len(data)

    for x_y in data:
	    sum_xy += x_y[0] * x_y[1]
	    sum_x += x_y[0]
	    sum_y += x_y[1]
	    sum_x2 += x_y[0] ** 2	
    
    a = (N * sum_xy - sum_x * sum_y)/float(N * sum_x2 -  sum_x ** 2)
    b = (sum_x2 * sum_y - sum_xy * sum_x)/float(N * sum_x2 - sum_x ** 2)

    return a, b