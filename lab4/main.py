def direct_run(volumes, values, capacity):
    item_count = len(volumes)
    dp = [[0] * (capacity + 1) for _ in range(item_count + 1)]
    decision = [[0] * (capacity + 1) for _ in range(item_count + 1)]

    for item_idx in range(1, item_count + 1):
        item_volume = volumes[item_idx - 1]
        item_value = values[item_idx - 1]

        for current_capacity in range(capacity + 1):
            if item_volume > current_capacity:
                dp[item_idx][current_capacity] = dp[item_idx - 1][current_capacity]
                decision[item_idx][current_capacity] = 0
            else:
                skip_value = dp[item_idx - 1][current_capacity]
                take_value = dp[item_idx - 1][current_capacity - item_volume] + item_value

                if take_value > skip_value:
                    dp[item_idx][current_capacity] = take_value
                    decision[item_idx][current_capacity] = 1
                else:
                    dp[item_idx][current_capacity] = skip_value
                    decision[item_idx][current_capacity] = 0

    return dp, decision


def reverse_run(dp, decision, volumes, capacity):
    selected = []
    remaining_capacity = capacity

    for item_idx in range(len(volumes), 0, -1):
        if decision[item_idx][remaining_capacity] == 1:
            selected.append(item_idx - 1)
            remaining_capacity -= volumes[item_idx - 1]

    selected.reverse()
    return dp[len(volumes)][capacity], selected


def print_table(table, title):
    print(f"\n{title}:")
    header = "     " + " ".join(f"{capacity:>4}" for capacity in range(len(table[0])))
    print(header)
    for idx, row in enumerate(table):
        formatted_row = " ".join(f"{value:>4}" for value in row)
        print(f"k={idx:>2} | {formatted_row}")


if __name__ == "__main__":
    volumes = [2, 5, 7, 3, 4, 6, 1, 8]  # Item volumes
    values = [5, 8, 12, 4, 6, 9, 4, 15]  # Item values
    capacity = 15  # Maximum knapsack capacity

    dp, decision = direct_run(volumes, values, capacity)
    max_value, selected = reverse_run(dp, decision, volumes, capacity)

   

    

    print_table(dp, "DP table (maximum value by prefix and capacity)")
    print_table(decision, "Decision table (1 - take item, 0 - skip item)")

    print("Selected items:")
    total_volume = 0
    for idx in selected:
        total_volume += volumes[idx]
        print(f"- Item {idx + 1}: volume={volumes[idx]}, value={values[idx]}")

    print(f"\nTotal volume used: {total_volume} / {capacity}")
    print(f"Total value: {max_value}")
