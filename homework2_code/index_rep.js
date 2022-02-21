const mysql = require('mysql2');
const express =  require('express');
const bodyParser = require('body-parser');

//connect to mysql database

var connection2 = mysql.createConnection({
	host: '35.222.245.110',
	port: '3306',
	user: 'master',
	password: 'masterpassword',
	database: 'mydb'
})



var connection = mysql.createConnection(
{
        host: '34.72.146.59',
	port: '3306',
        user: 'master',
        password: 'masterpassword',
        database : 'mydb'
})

connection2.connect(function(e){

	if(e){
		throw e;
	}
	console.log("Connected");
})

connection.connect(function(e){
	if(e){
		throw e;
	}{
	
		console.log("Connected to rep");
	}
});

//init webapp
const app = express();
app.use(bodyParser.json());


//greeting, part 1
app.get('/greeting', (req,res)=>{
        res.end("Hello World!");
})


/////PART 2////////

// register post req
app.post('/register',(req,res)=>{
        let n =  req.body.username;
        n = n.replace(/^[0-9\s]*|[+*\r\n]/g, '');
        let query = `INSERT INTO Users (username) VALUES ('`+n+`');`; 
        connection.query(query, (e,r,f)=>{
                res.json({'message': 'Success', 'username:' : r});
        });
})

//list get req
app.get('/list', (req,res)=>{
        let query = `SELECT * FROM Users;`;
        connection.query(query,(e,r,f)=>{
                let arr = []
                for(var  i = 0; i < r.length; i++){
                        arr.push(r[i].username);
                }
                console.log(arr);
                res.json({'users': arr });
        })
})

//clear post req
app.post('/clear', (req,res)=>{
        let query = `DELETE FROM Users;`;
        connection.query(query, (e,r,f)=>{
                res.end("deleted");
        });
})







//http res for listening
var http = require('http').Server(app);
const PORT = 80;
http.listen(PORT, function(){
        console.log('Listenning');
})


