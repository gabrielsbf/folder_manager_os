import datetime as dt

# print(dt.datetime.strftime(dt.datetime.now(), "%y%m%d"))

sep = ["join_t"]
old_arr = ["alal", "teste1", "oskey"]

new = list(map(lambda x : (x + "/").join(sep) , old_arr))
print(new)