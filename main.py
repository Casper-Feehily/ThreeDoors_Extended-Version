import random
import math

def simulate_extended_monty_hall(num_doors: int, num_host_opens: int, switch: bool, trials: int = 100):
    if num_doors < 3:
        raise ValueError("🚪 门的数量必须至少为 3 扇。")
    if num_host_opens >= num_doors - 1:
        raise ValueError("🎭 主持人必须至少留两扇门未打开（一个供选择，一个可能是奖品）。")

    wins = 0
    results = []

    for _ in range(trials):
        doors = [0] * (num_doors - 1) + [1]  # 1 代表奖品，其他门为空
        random.shuffle(doors)

        choice = random.randint(0, num_doors - 1)  # 参赛者的初始选择

        # 主持人打开若干扇没有奖品的门，且不是参赛者选择的门
        available_doors = [i for i in range(num_doors) if i != choice and doors[i] == 0]
        host_opens = random.sample(available_doors, num_host_opens)

        # 如果选择更换门，则从剩余未打开的门中随机选择
        if switch:
            remaining_doors = [i for i in range(num_doors) if i != choice and i not in host_opens]
            choice = random.choice(remaining_doors)

        win = doors[choice] == 1
        wins += win
        results.append(win)  # 只存储布尔值结果，不包含颜色代码

    win_probability = wins / trials
    return results, win_probability

# 获取用户输入的门的数量和主持人要打开的门的数量
num_doors = int(input("🎯 请输入门的总数（至少 3 扇）："))
num_host_opens = int(input(f"🔑 请输入主持人要打开的门的数量（必须小于 {num_doors - 1}）："))



# 运行模拟，使用更换选择策略
simulation_results, probability = simulate_extended_monty_hall(num_doors, num_host_opens, switch=True, trials=10000) #在这里调整模拟次数

# 计算合适的矩阵大小
matrix_size = math.isqrt(len(simulation_results))
if matrix_size ** 2 < len(simulation_results):
    matrix_size += 1

print("\n📊 实验结果矩阵（中奖/不中奖）：")
for i in range(matrix_size):
    row_indices = range(i * matrix_size, min((i + 1) * matrix_size, len(simulation_results)))
    # 将布尔值转换为带颜色的字符串，但在打印时计算其实际显示宽度
    formatted_row = []
    for j in row_indices:
        if simulation_results[j]:  # 如果是True（中奖）
            formatted_row.append("\033[92m中奖\033[0m")  # 绿色
        else:
            formatted_row.append("\033[91m不中奖\033[0m")  # 红色

    # 打印一行，使用固定宽度的空格
    print("  ".join(formatted_row))

# 计算不换门的理论中奖概率
theoretical_no_switch_probability = 1 / num_doors
print(f"\n🎲 不换门的理论中奖概率: {theoretical_no_switch_probability:.5f}")

# 输出实际模拟结果
print(f"\n✨ 在 {num_doors} 扇门、主持人打开 {num_host_opens} 扇门的情况下，选择更换门的中奖概率: {probability:.5f}")
