import wikipedia
import wolframalpha

while True:
        input = raw_input("Q: ")

        try:
            #wolframalpha
            app_id = "K7PUL4-AW9W933275"
            client = wolframalpha.Client(app_id)
            res = client.query(input)
            answer = next(res.results).text
            print answer
        except:
            #wikipedia
            print wikipedia.summary(input)
