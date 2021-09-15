## Chatbot vaanah

1- build image
docker build -t vaanah/chatbot:latest .
2- run image
docker run -tid -p 8080:8000 --name bot vaanah/chatbot:latest

# URL API

http://localhost:8080/bot?msg=[your message]

## Example

http://localhost:8080/bot?msg='who are you ?'

> > "I am a virtual agent."
