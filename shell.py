from run import run

while True:
    text = input("basic > ")
    result, error = run(text)

    if error:
        print(error.as_string())
    elif result:
        print(result)
