import speech_recognition as sr 
import pyttsx3
import datetime
import webbrowser
import pyaudio
import wave
import wikipedia
import wolframalpha


class assistant():
	def __init__(self,engine=None,recognizer=None,microphone=None):
		self.engine=pyttsx3.init() or engine
		self.recognizer=sr.Recognizer() or recognizer
		self.microphone=sr.Microphone() or microphone
		voices=self.engine.getProperty("voices")
		self.engine.setProperty("rate",110)
		self.engine.setProperty("voice",voices[11].id)
		

	def speak(self,sentence,engine=None):
		engine= engine or self.engine
		print(sentence)
		engine.say(sentence)
		engine.runAndWait()

	def listen(self,micro=None,rec=None):
		micro=micro or self.microphone
		rec=rec or self.recognizer
		with micro as source:
			rec.adjust_for_ambient_noise(source,duration=1)
			print("Listening...")
			audio=rec.listen(source,phrase_time_limit=7)
			#print("Just a second,I'm thinking.")

		try:
			l=rec.recognize_google(audio)
		except:
			l="I'm sorry I couldn't understand that."

		print("Q:",l.capitalize())
		return l

	def asked_date(self):
		today=datetime.datetime.today()
		info="Today is "+datetime.datetime.strftime(today,"%d %B %Y %A")
		self.speak(info)

	def asked_time(self):
		hour=datetime.datetime.today()
		info="The time is "+datetime.datetime.strftime(hour, "%X")
		self.speak(info)

	def play(self,filepath):
		
		filename = filepath
		# Set chunk size of 1024 samples per data frame
		chunk = 1024  
		# Open the sound file 
		wf = wave.open(filename, 'rb')
		# Create an interface to PortAudio
		p = pyaudio.PyAudio()
		# Open a .Stream object to write the WAV file to
		# 'output = True' indicates that the sound will be played rather than recorded
		stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
		                channels = wf.getnchannels(),
		                rate = wf.getframerate(),
		                output = True)
		# Read data in chunks
		data = wf.readframes(chunk)
		# Play the sound by writing the audio data to the stream
		while data != '':
			stream.write(data)
			data = wf.readframes(chunk)
			if not data:
				stream.stop_stream()
				stream.close()
				p.terminate()
				break

	def wiki(self,query):
		print("entered function with:",query)
		query=query.split(" ")
		try:
			a=query.index("search")
			b=query.index("in")
			word=query[a+1:b]
			print("lookiing for:",word)
			try:
				result=wikipedia.summary(word,sentences=2)
				self.speak(result)
				print(result)
			except:
				self.speak("I'm sorry,I couldn't find anything.")
		except:
			self.speak("Sorry,couldn't parse the query.")


	def wolfram(self,sentence):
		server = 'http://api.wolframalpha.com/v1/query.jsp'
		appid = 'API Key'
		try:
			client = wolframalpha.Client(appid)
			res = client.query(sentence)
			print(type(res.results))
			self.speak(next(res.results).text)
		except:
			self.speak("Sorry,something went wrong.")
		

	def main(self):
		#self.speak("Hi, it good to see you.Please don't mind the mess above.")
		while True:
			self.speak("Is there anything I can do for you?")
			query=self.listen()
			

			if ("close" in query) or ("quit" in query) or ("exit" in query):
				self.speak("Okay,see you later.")
				break

			elif "date" in query:
				self.asked_date()

			elif ("time" in query) or ("hour" in query):
				self.asked_time()

			elif "wikipedia" in query or "Wikipedia" in query:
				self.wiki(query)

			else :
				if(("search" in query)):
					query=query.split(" ")
					a=query.index("search") 
					query=query[a+1:]
				self.wolfram(query)









assistant=assistant()
assistant.main()