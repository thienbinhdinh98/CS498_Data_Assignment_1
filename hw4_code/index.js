var exec = require('ssh-exec');
const fs = require('fs');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());



app.post('/results', (req,res)=>{
	let term = req.body.term
	let cmd = `python3 pythonres.py ${term}`;
	console.log(cmd);
	exec(cmd, {
		user: 'thienbinhdinh98',
		host: '10.128.0.6',
		key: fs.readFileSync('../c')
	},function(err, stdout, stderr){
		console.log(err, stdout, stderr);
		let new_out = stdout

		let dict = {};
		dict['results'] = {};
		let g = JSON.parse(new_out.replace(/\u0027/g,'"'));
		console.log(typeof(g))
		console.log(g);
		for(const key in g){
			dict['results'][key] = g[key]
		}
		res.json(dict);
	})
})

app.post('/trends',(req,res)=>{
	let term =  req.body.term
	let cmd = `python3 pythontrend.py ${term}`;
	console.log(cmd);
	exec(cmd, {
		user: 'thienbinhdinh98',
		host: '10.128.0.6',
		key: fs.readFileSync('../c')
	},function(err, stdout, stderr){
		console.log(err, stdout, stderr);
		let num = parseInt(stdout)
		console.log(num, typeof(num))
		res.json({"clicks": num})

	})
})


app.post('/popularity', (req,res)=>{
	let url = req.body.url
	let cmd = `python3 pythonpop.py ${url}`;
	console.log(cmd);
	exec(cmd, {
		user: 'thienbinhdinh98',
		host: '10.128.0.6',
		key: fs.readFileSync('../c')
	},function(err,stdout, stderr){
		console.log(err, stdout, stderr);
		let num = parseInt(stdout);
		console.log(num, typeof(num));
		res.json({"clicks":num})
	})
})

app.post('/getBestTerms', (req,res)=>{
	let site = req.body.website
	let cmd = `python3 best.py ${site}`
	console.log(cmd);
	exec(cmd, {
		user: 'thienbinhdinh98',
		host: '10.128.0.6',
		key: fs.readFileSync('../c')
	},function(err, stdout,stderr){
		console.log(err, stdout,stderr);
		let ans = stdout.replace("\n" , "");
		let arr = ans.split(',');
		res.json({"best_terms": arr});
	})



})

var http = require('http').Server(app);
const PORT = 80;
http.listen(PORT, function(){
	console.log('Listenning');
})
