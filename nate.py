import wx
import wikipedia
import wolframalpha
import speech_recognition as sr
import pyaudio as p

from espeak import espeak

espeak.synth("Welcome")

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          pos=wx.DefaultPosition,
                          size=wx.Size(450, 100),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                          wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                          title="Nate")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,
                            label="Hello I am Nate the python Digital Assistant. How may i help you?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def OnEnter(self, event):
        input = self.txt.GetValue()
        input = input.lower()

        if input == '':
            if p.PyAudio().get_device_count() <= 0:
                espeak.synth("I apologize, but you don't have an available microphone.")
            else:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = r.listen(source)
                try:
                    self.txt.SetValue(r.recognize_google(audio))
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

        try:
            app_id = "K7PUL4-AW9W933275"
            client = wolframalpha.Client(app_id)
            res = client.query(input)
            answer = next(res.results).text
            print(answer)
            espeak.synth("The answer is " + answer)
        except:
            if len(input) >= 1:
                input = input.split(' ')
                input = " ".join(input[2:])
            print(len(input))
            if input != '':
                espeak.synth("Searched for "+input)
                print(wikipedia.summary(input))
            else:
                espeak.synth("I am sorry, but you wrote nothing.")
            #espeak.synth()

if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()
