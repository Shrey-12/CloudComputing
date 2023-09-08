const mysql = require('mariadb')
const endpoint = require("endpoint")
// create a connection pool
const pool = mysql.createPool({
    host: endpoint,
    user:'user',
    password:'user1234',
    database:'nodeAppDB',
    waitForConnections:true,
    connectionLimit:10,
    queueLimit:0
});

module.exports = pool
