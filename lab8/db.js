const mysql = require('mariadb')

const pool = mysql.createPool({
		host: "localhost",
		user: 'user',
		password: 'pass123',
		database: 'lab5',
		waitForConnection:true,
		connectionLimit:10,
		queueLimit:0
});

module.exports = pool
