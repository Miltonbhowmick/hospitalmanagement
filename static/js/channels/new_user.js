$ (function () {
      endpoint = 'ws: //127.0.0.1: 8000 / new-user /' // 1

      var socket = new ReconnectingWebSocket (endpoint) // 2
      
     // 3
      socket.onopen = function (e) {
        console.log ("open", e); 
      }
      socket.onmessage = function (e) {
        console.log ("message", e)
        var userData = JSON.parse (e.data)
        $('# new_user'). html (userData.html_users)
      }
      socket.onerror = function (e) {
        console.log ("error", e)
      }
      socket.onclose = function (e) {
        console.log ("close", e)
      }
 });