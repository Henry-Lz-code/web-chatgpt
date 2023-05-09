# -*- coding: UTF-8 -*-

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/chatgpt/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


html2 = """
<!DOCTYPE html>
<html>
  <head>
    <title>Chat</title>
    <style>
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
          font-family: Arial, Helvetica, sans-serif;
        }

        body {
          background-color: #f6f6f6;
          display: flex;
          flex-direction: column;
          height: 100vh;
        }

        h1 {
          font-size: 2rem;
          margin: 20px 0;
          text-align: center;
        }

        h2 {
          font-size: 1.5rem;
          margin-bottom: 10px;
          text-align: center;
        }

        form {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin: 20px;
        }

        input[type="text"] {
          border: none;
          border-radius: 20px;
          padding: 10px;
          width: 80%;
          background-color: #f0f0f0;
        }

        button {
          border: none;
          border-radius: 20px;
          padding: 10px 20px;
          background-color: #338eff;
          color: #fff;
          font-weight: bold;
          cursor: pointer;
          transition: background-color 0.3s;
        }

        button:hover {
          background-color: #2974ca;
        }

        ul {
          list-style: none;
          flex-grow: 1;
          overflow-y: scroll;
        }

        li {
          margin: 10px;
          padding: 10px;
          border-radius: 20px;
          max-width: 80%;
        }

        #messages {
          display: flex;
          flex-direction: column;
          align-items: flex-end;
        }

    </style>
  </head>
  <body>
    <div class="container">
      <header>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
      </header>
      <main>
        <ul id="messages"></ul>
        <form action="" onsubmit="sendMessage(event)">
          <input type="text" id="messageText" autocomplete="off" placeholder="输入消息...">
          <button type="submit">发送</button>
        </form>
      </main>
    </div>
    <script>
      var client_id = Date.now();
      document.querySelector("#ws-id").textContent = client_id;
      var ws = new WebSocket(`ws://localhost:8000/test/ws/${client_id}`);
      ws.onmessage = function (event) {
        var messages = document.getElementById("messages");
        var message = document.createElement("li");
        var content = document.createTextNode(event.data);
        message.appendChild(content);
        messages.appendChild(message);
      };
      function sendMessage(event) {
        var input = document.getElementById("messageText");
        ws.send(input.value);
        input.value = "";
        event.preventDefault();
      }
    </script>
  </body>
</html>
"""


chat_html = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>ChatGPT</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
      body {
        background-color: whitesmoke;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
      }
      .chat-container {
        max-width: 1500px;
        margin: 50px auto;
        border: 1px solid burlywood;
        border-radius: 5px;
        background-color: lightsteelblue;
        overflow: hidden;
      }
      .chat-header {
        background-color: lightpink;
        border-bottom: 1px solid #ddd;
        padding: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        top: 0;
        z-index: 1;
        width: 1500px;
      }
      .chat-header img {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        margin-right: 10px;
      }
      .chat-header h5 {
        margin: 0;
        font-weight: 500;
        font-size: 18px;
      }
      .chat-messages {
        padding: 10px;
        min-height: 820px;
        # max-height: 800px;
        margin-bottom: 2px;
        overflow-y: auto;
      }
      .chat-message-user {
        display: flex;
        margin-bottom: 10px;
      }
      .chat-message-sys {
        display: flex;
        margin-bottom: 10px;
      }
      .avatar {
        width: 50px;
        height: 50px;
        border-radius: 1px;
        margin-right: 5px;
      }
      .chat-message-user .message-content {
        background-color: mediumspringgreen;
        border-radius: 10px;
        padding: 10px;
        max-width: 80%;
        word-wrap: break-word;
      }
      .chat-message-sys .message-content {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        max-width: 80%;
        word-wrap: break-word;
      }
      .chat-message .message-time {
        font-size: 12px;
        color: #aaa;
        margin-left: 10px;
        align-self: flex-end;
      }
      .chat-input {
        background-color: #fff;
        padding: 10px;
        display: flex;
        align-items: center;
        border: 1px solid burlywood;
        border-radius: 5px;
        position: fixed;
        bottom: 1px;
        z-index: 1;
        width: 1500px;
      }
      .chat-input input {
        flex-grow: 1;
        border: none;
        border-radius: 20px;
        padding: 10px;
        font-size: 14px;
        outline: none;
      }
      .chat-input button {
        background-color: #0084ff;
        color: #fff;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 14px;
        margin-left: 10px;
        cursor: pointer;
      }
    </style>
  </head>
  <body>
    <div class="chat-container">
      <div class="chat-header">
        <h5>Your Jarvis</h5>
      </div>
      <div class="chat-messages">

      </div>
      <div class="chat-input">
        <input type="text" placeholder="请输入你的问题。。。。">
        <button><i class="far fa-paper-plane"></i></button>
      </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
      // request ws
      let client_id = Date.now();
      let ws = new WebSocket(`ws://${window.location.host}/chat/ws/${client_id}`);
      // ws.onmessage = function(event) {
      //   let content = event.data;
      //   let input_str = '<div class="chat-message-sys"><img class="avatar" src="https://i-1.rar8.net/2023/2/24/e7a2033b-c04e-418c-a1a8-0c3a109557d1.png" alt="System"><div class="message-content">' + content + '</div></div>'
      //   $(".chat-messages").append(input_str);
      //   $(".chat-messages").scrollTop($(".chat-messages")[0].scrollHeight);
      // };
      let messageBuffer = "";  // 用于缓存消息的变量
      let $messageContainer = null;  // 用于存储消息的子div标签

      ws.onmessage = function(event) {
        let content = event.data;
        if (content === "stop") {
          // 如果收到了stop消息，将存储消息的变量添加到已有的子div标签中，并将存储消息的变量清空
          if (messageBuffer !== "") {
            messageBuffer = "";
          }
          $messageContainer = null;  // 重置存储消息的子div标签
        } else {
          // 如果收到了非stop消息
          if ($messageContainer === null) {
            // 如果还不存在存储消息的子div标签，添加一个空的子div标签
            $messageContainer = $('<div class="chat-message-sys"><img class="avatar" src="https://i-1.rar8.net/2023/2/24/e7a2033b-c04e-418c-a1a8-0c3a109557d1.png" alt="System"><div class="message-content"></div></div>');
            $(".chat-messages").append($messageContainer);
          }
          // 将接收到的消息追加到已有的子div标签内容中
          messageBuffer += content;
          $messageContainer.find(".message-content").html(messageBuffer);
          $(".chat-messages").scrollTop($(".chat-messages")[0].scrollHeight);
        }
      };
      function sendMessage(event) {
          var input = document.getElementById("messageText")
          ws.send(input.value)
          input.value = ''
          event.preventDefault()
      }
      // Scroll to the bottom of the chat messages
      $(".chat-messages").scrollTop($(".chat-messages")[0].scrollHeight);
      // Send message on button click
      $("button").click(function() {
        let message = $("input").val();
        if (message != "") {
          // ws发送数据
          ws.send(message)
          let input_str = '<div class="chat-message-user"><img class="avatar" src="https://picx.zhimg.com/v2-a962d6c4a6258ca7d6645742085fb564_r.jpg?source=1940ef5c" alt="User"><div class="message-content">' + message + '</div></div>'
          $(".chat-messages").append(input_str);
          $("input").val("");
          $(".chat-messages").scrollTop($(".chat-messages")[0].scrollHeight);
        }
      });

      // Send message on enter key press
      $("input").keypress(function(e) {
        if (e.which == 13) {
          $("button").click();
        }
      });

      // Get current time
      function getTime() {
        let now = new Date();
        let hours = now.getHours();
        let minutes = now.getMinutes();
        let ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12;
        minutes = minutes < 10 ? '0'+minutes : minutes;
        let time_str = hours + ':' + minutes + ' ' + ampm;
        return time_str;
      }
    </script>
  </body>
</html>"""
