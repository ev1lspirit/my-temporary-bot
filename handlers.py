import statistics
from telethon.events import NewMessage
from utils import split_generator, splitters, apply_weights, target_words_weight, epsilon


async def calculate_weights_handler(event: NewMessage.Event):
    message_weight = (
            apply_weights(split_generator(splitters, event.message.message), target_words_weight))
    message_mean = statistics.mean(message_weight.values())
    se = map(lambda x: (x[0], x[1] ** 2 - message_mean ** 2), message_weight.items())
    total_sum = sum(map(lambda x: x[1], se))
    return total_sum, total_sum >= epsilon