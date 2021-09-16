## Chatbot vaanah

1- build image
docker build -t vaanah/chatbot:latest .
2- run image
docker run -tid -p 8080:8000 --name bot vaanah/chatbot:latest

# URL API

Method: POST

http://localhost:8080/api/bot

Request body raw:

## Example

POST
http://localhost:8080/api/bot
{
msg: "Who are you ?"
}

return:
{
message: "I am a virtual agent."
}
