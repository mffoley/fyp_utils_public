const functions = require("firebase-functions");


const express = require('express');
const cors = require('cors');
// const Deals = require('./config')

var  admin = require("firebase-admin");

var serviceAccount = require("./finalyearproject-b132e-a22a1ab9e8e9.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://finalyearproject-b132e-default-rtdb.firebaseio.com/"
});

var db = admin.database();
var ref = db.ref("restricted_access/secret_document");

ref.on("value", function(snapshot) {
  console.log(snapshot.val());
}, function (errorObject) {
  console.log("The read failed: " + errorObject.code);
});


const votesRef = db.ref('routes'); //ref.child('votes');

const app = express();

//app.use(express.json())
app.use(cors());

app.get("/api/routevotes", async (req, res) => {
  console.log("test");

  votesRef.on("value", function(snapshot) {
    console.log(snapshot.val());
    res.send(snapshot.val());
  }, function (errorObject) {
    console.log("why doesnt this work? "+errorObject.code);
  });
});


app.get("/api/votes/csv", async (req, res) => {
  console.log("test");

  votesRef.on("value", function(snapshot) {
    var csv = "id,votes,lat,long";
    var data = snapshot.val();
    for (var key in data) {
      if (data.hasOwnProperty(key)) {
        csv += "\n"+key+","+data[key]["votes"]+","+data[key]["lat"]+","+data[key]["long"];
      }
    }

    res.send(csv);
  }, function (errorObject) {
    console.log("why doesnt this work? "+errorObject.code);
  });
});

//has to be a get to be accesible from arcgis 

app.get('/api/votes/:id/increment', async (req, res) => {
  const id = req.params.id;

  votesRef.child(id).once("value", function(snapshot) {
    var votes = 1;
    var data = snapshot.val();
    if(data !== null){
      votes += data["votes"];
    }
    votesRef.update({ [id] : {votes: votes, lat: data.lat, long: data.long}});
    res.sendFile(__dirname + '/voted.html');
  }, function (errorObject) {
    console.log("why doesnt this work? "+errorObject.code);
    res.send("error");
  });
});
  


app.post('/api/votes', async (req, res) => {
  const data = req.body;
  console.log(data);

  var batchedIds = {};

  //JSON.parse(data.routes).forEach(element => {
  data.forEach(element => {
    batchedIds[element.id] = {votes: Math.floor(Math.random()*1000), lat: element.lat, long: element.long};
  });
  votesRef.update(batchedIds);
  res.send({ msg: "Added" });
});


  exports.app = functions.https.onRequest(app);