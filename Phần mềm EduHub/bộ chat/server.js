const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { maxHttpBufferSize: 1e7 });

// PHỤC VỤ FILE TĨNH: Cho phép truy cập tất cả file trong thư mục
app.use(express.static(__dirname));

// ĐƯỜNG DẪN TRANG CHỦ -> Mở Dashboard
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'dashboard.html'));
});

// ĐƯỜNG DẪN PHÒNG CHAT
app.get('/chat', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// --- LOGIC CHAT (GIỮ NGUYÊN) ---
let lichSuTinNhan = [];
let users = {};
const MAT_KHAU_GV = "123456";

io.on('connection', (socket) => {
    socket.emit('tai-lich-su', lichSuTinNhan);
    socket.on('dang-nhap', ({ ten, matKhau }) => {
        socket.data.username = ten;
        users[socket.id] = ten;
        if (matKhau === MAT_KHAU_GV) socket.emit('quyen-admin', true);
        io.emit('cap-nhat-online', Object.values(users));
    });

    socket.on('gui-tin-nhan', (noiDung) => {
        const tin = { id: Date.now(), ten: socket.data.username, content: noiDung, type: 'text', time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) };
        lichSuTinNhan.push(tin);
        io.emit('nhan-tin-nhan', tin);
    });

    socket.on('disconnect', () => {
        delete users[socket.id];
        io.emit('cap-nhat-online', Object.values(users));
    });
});

server.listen(3000, () => console.log('Hệ thống chạy tại: http://localhost:3000'));