const mysql = require('mariadb')

const pool = mysql.createPool({
		host: "localhost",
		user: 'shreya',
		password: 'shreya123',
		database: 'lab5',
		waitForConnection:true,
		connectionLimit:10,
		queueLimit:0
});

module.exports = pool
