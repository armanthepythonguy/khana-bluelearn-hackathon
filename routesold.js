const express = require('express');
const router = express.Router();
const db = require('../config/dbConnection');

router.post('/byName', async (req, res) => {
    if (db.get() == null) res.send("DB not running");
    else {
        const stationCode = req.body.stationCode
        const name = req.body.name
        if(stationCode == null || name == null){
            res.send({ok:"false", msg:"Invalid Name or Station Code"})
        }
        await db.get().collection('cases').find({stationCode:stationCode, name:name}).toArray()
            .then(response => {
                if(response!=[]){
                    res.send(response)
                }
                else{
                    res.send({ok:"false",msg:"Case Details not found"})
                }
            })
            .catch(error => res.send(error.errmsg || error.name))
    }
});

router.post('/search', async (req, res) => {
    if (db.get() == null) res.send("DB not running");
    else {
        const stationCode = req.body.stationCode
        const search = "^"+req.body.search
        if(stationCode == null){
            res.send({ok:"false", msg:"Invalid Name or Station Code"})
        }
        if(stationCode == "AAAA"){
            await db.get().collection('cases').find({},{projection: {name:1,ps: 1, crNo:1, _id:0}}).toArray()
            .then(response => {
                if(response!=[]){
                    res.send(response)
                }
                else{
                    res.send({ok:"false",msg:"Case Details not found"})
                }
            })
            .catch(error => res.send(error.errmsg || error.name))
        }
        else {
        await db.get().collection('cases').find({stationCode:stationCode, name:{$regex:search, $options : 'i'}}).toArray()
            .then(response => {
                if(response!=[]){
                    res.send(response)
                }
                else{
                    res.send({ok:"false",msg:"Case Details not found"})
                }
            })
            .catch(error => res.send(error.errmsg || error.name))
        }
    }
});

router.post('/byStationCode', async (req, res) => {
    if (db.get() == null) res.send("DB not running");
    else {
        const stationCode = req.body.stationCode
        if(stationCode == null){
            res.send({ok:"false", msg:"Invalid Name or Station Code"})
        }
        else{
            await db.get().collection('cases').find({stationCode:stationCode}).toArray()
            .then(response => {
                if(response!=[]){
                    res.send(response)
                }
                else{
                    res.send({ok:"false",msg:"Case Details not found"})
                }
            })
            .catch(error => res.send(error.errmsg || error.name))
        }
    }
});

router.post('/add', async (req, res) => {
    if (db.get() == null) res.send("DB not running");
    else {
        await db.get().collection('cases').insertOne(req.body)
            .then(() => { res.send({"ok":"true", "msg":"Data Inserted"}) })
            .catch(error => res.send(error.errmsg || error.name))
    }
});

router.post('/delete', async (req, res) => {
    if (db.get() == null) res.send("DB not running");
    else {
        console.log(req.body._id)
        await db.get().collection('cases').remove({ _id: new mongodb.ObjectID(req.body._id) })
            .then((result) => {
                console.log(result)
               //Check if deleted and send response
            })
            .catch(error => res.send(error.errmsg || error.name))
    }
});

module.exports = router;