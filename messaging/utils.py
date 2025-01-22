
def calculate_typing_delay_seconds(message: str) -> float:
    num_chars = len(message)
    total_delay = (num_chars * 0.1) + ((num_chars - 1) // 20 * 0.5)
    return total_delay  # Returns delay in seconds
