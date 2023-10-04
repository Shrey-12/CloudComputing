const express = require('express');
const app = express();
const pool = require('./db');
var bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/', express.static('./'));

const query = `CREATE TABLE IF NOT EXISTS feedback (
		id INT NOT NULL AUTO_INCREMENT,
		name VARCHAR(255) NOT NULL,
		message VARCHAR(255) NOT NULL,
		PRIMARY KEY (id)
)`;

const query2 = `CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	PRIMARY KEY (id)
)`;

const query3=`CREATE TABLE IF NOT EXISTS likes (
	id INT NOT NULL AUTO_INCREMENT,
	count INT NOT NULL DEFAULT 0,
	PRIMARY KEY (id)
  );  
`

const query4=`INSERT INTO users (name) VALUES ('Shreya')`;
const query5=`INSERT INTO likes (count) VALUES (0)`;


pool.getConnection().then(async (connection) => {
		try {
				await connection.query(query);
				await connection.query(query2);
				await connection.query(query3);
				await connection.query(query4);
				await connection.query(query5);
				connection.commit();
		} catch (err) {
				console.error('Error Creating Table:', err);
		} finally {
				connection.close()
		} 
});

app.get('/feedback', (req, res) => {
		res.sendFile(__dirname + '/feedback.html');
});


app.get('/changeName', (req, res) => {
	res.sendFile(__dirname + '/changename.html');
});

app.get('/like', (req, res) => {
	res.sendFile(__dirname + '/like.html');
});

app.get('/comments', (req, res) => {
		pool.getConnection().then( async (connection) => {
				try {
						const rows = await connection.query("SELECT name,message from feedback");
						let out = `<html>
								<head><title>Comments</title></head><body><br><br><center>` ;
						for(let i = 0; i < rows.length; i++){
								out = out + rows[i].name + ":" + rows[i].message + "<br><br>";
						}
						out = out + "<a href='/'>Go Back</a></center></body></html>"
						res.send(out);
				} catch (err) {
						console.error("Error retreiving data:",err);
				} finally {
						connection.close();
				} 
		});
});

app.post('/feedback', (req, res) => {
		const name = req.body.name;
		const message = req.body.message;
		pool.getConnection().then( async (connection) => {
				try {
						await connection.query("INSERT INTO feedback (name, message) VALUES (?,?)", [name, message]);
						connection.commit();
						res.redirect("/comments");
				} catch (err) {
						console.error("Error inserting data:", err);
						res.status(500).send("Error inserting data.")
				} finally {
						connection.close()
				}
		});
});

app.post('/change-name',(req,res)=>{
	const newName=req.body.newName;
	const id=1;
	pool.getConnection().then(async(connection)=>{
		try{
			await connection.query("UPDATE users SET name=? WHERE id=?",[newName,id]);
			connection.commit();
			res.redirect("/");
		}catch(err){
			console.log("Error updating name:",err);
			res.status(500).send("Error updating name");
		}finally{
			connection.close();
		}
	})
})

app.get('/set-name', async (req, res) => {
	const userId = 1; 
	const result = await pool.query('SELECT name FROM users WHERE id=?', [userId]);
	const userName = result[0].name;
	res.json({ name: userName });
  });

app.get('/get-like-count', async (req, res) => {
pool.getConnection().then(async (connection) => {
	try {
	const result = await connection.query('SELECT count FROM likes WHERE id = 1');
	const likeCount = result[0].count;
	res.json({ count: likeCount });
	} catch (err) {
	console.error('Error retrieving like count:', err);
	res.status(500).send('Error retrieving like count.');
	} finally {
	connection.release();
	}
});
});

// Increment the like count in the database
app.post('/increment-like-count', async (req, res) => {
pool.getConnection().then(async (connection) => {
	try {
	// Increment the like count by 1
	await connection.query('UPDATE likes SET count = count + 1 WHERE id = 1');
	res.sendStatus(200);
	} catch (err) {
	console.error('Error incrementing like count:', err);
	res.status(500).send('Error incrementing like count.');
	} finally {
	connection.release();
	}
});
});

const port  = process.env.PORT || 8080;
console.log(port)
app.listen(port, ()=>{
		console.log("started");
});
