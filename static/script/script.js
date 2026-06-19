const socket = io();
const roomId = document.getElementById('room-data').dataset.roomId;

socket.emit('join', { room_id: roomId });

document.getElementById('message-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const input = document.getElementById('message-input');
  const content = input.value.trim();
  if (!content) return;

  socket.emit('send_message', { room_id: roomId, content: content });
  input.value = '';
});

socket.on('new_message', (data) => {
  const messages = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'mb-2';
  const name = document.createElement('strong');
  name.textContent = data.username;
  const body = document.createElement('div');
  body.textContent = data.content;
  div.appendChild(name);
  div.appendChild(body);
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
});
