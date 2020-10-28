#
# def contains_3(where: str, what: str) -> bool:
#     count = 0
#     for i in range(len(where) - len(what) + 1):
#         for j in range(len(what)):
#             if where[i + j] == what[j]:
#                 count += 1
#             if where[i + j] != what[j]:
#                 count = 0
#             if count == len(what):
#                 return True
#     return False


def contains_4(where: str, what: str) -> bool:
    for i in range(len(where) - len(what)+1):
        count = 0
        for j in range(len(what)):
            if where[i + j] == what[j]:
                count += 1
        if count == len(what):
            return True
    return False




# # читерский
# def contains_second(where: str, what: str) -> bool:
#     for i in range(len(where) - len(what)):
#         if where[i: i + len(what)+1] == what:
#             return True
#     return False
#
# # честный
# def contains_second(where: str, what: str) -> bool:
#     for i in range(len(where) - len(what)+1):
#         count = 0
#         for j in range(len(what)):
#             if where[i + j] == what[j]:
#                 count += 1
#             else:
#                 break
#
#         if count == len(what):
#             return True
#
#     return False
#
# # честный со свернут внутренним циклом
# def contains_second(where: str, what: str) -> bool:
#     for i in range(len(where) - len(what)+1):
#         if all(where[i + j] == what[j] for j in range(len(what))):
#             return True
#     return False
#
# # честный со свернутым внешним и внутренним циклом
# def contains_second(where: str, what: str) -> bool:
#     return any(all(where[i + j] == what[j] for j in range(len(what))) for i in range(len(where) - len(what)+1))
#
# # читерский со свернутым циклом
# def contains_second(where: str, what: str) -> bool:
#     return any(where[i: i + len(what)] == what for i in range(len(where) - len(what)+1))