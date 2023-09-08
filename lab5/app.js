const express = require('express');
const app = express();
const pool = require('./db');
var bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use('/', express.static('./'));

// Create the table when the application starts
const tableName = 'feedback';
const query = `CREATE TABLE IF NOT EXISTS ${tableName} (
    id INT NOT NULL PRIMARY AUTO_INCREMENT,
    rating INT NOT NULL,
    message VARCHAR(255) NOT NULL
)`;

pool.getConnection().then(async (conn) => {
    try {
        await conn.query(query);
        conn.commit();
    } catch (err) {
        console.error("Error creating table:", err);
    } finally {
        conn.end();
    }
});

app.get('/review.html', function (req, res) {
    res.sendFile(__dirname + '/review.html');
});

app.get('/', (req, res) => {
    // Your root route logic here
});

app.post('/review.html', function (req, res) {
    const rating = req.body.rating;
    const message = req.body.message;

    console.log(req.body);
    pool.getConnection().then(async (conn) => {
        try {
            await conn.query("INSERT INTO feedback (rating, message) VALUES (?, ?)", [rating, message]);
            conn.commit();
            res.redirect("/");
        } catch (err) {
            console.error("Error inserting data:", err);
            res.status(500).send("Error inserting data.");
        } finally {
            conn.end();
        }
    });
});

app.listen(80);
