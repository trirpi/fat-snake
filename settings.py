# game settings
window_width = 1000
window_height = 1000

food_num = 1000

a = [100 + round(0.05*(1.1**x)) for x in reversed(range(100))]
rounds_with_dangerous_snake = [sum(a[:t]) for t in range(len(a))]
rounds_with_sticky_snake = [2500, 5000, 10000]
