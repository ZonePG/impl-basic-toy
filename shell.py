from run import run


while True:
    text = input("basic > ")
    if text.strip() == "":
        continue
    result, error = run("<stdin>", text)

    if error:
        print(error.as_string())
    elif result:
        if len(result.elements) == 1:
            # print("Result: ")
            print(repr(result.elements[0]))
        else:
            # print("Result: ")
            print(repr(result))
