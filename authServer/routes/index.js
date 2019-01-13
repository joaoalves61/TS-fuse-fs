var express = require('express');
var router = express.Router();
var fs = require('fs')
const nacl = require('tweetnacl')
const utils = require('tweetnacl-util')
const encodeBase64 = utils.encodeBase64

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index');
});

router.post('/verifyCode', (req,res) => {
  var result = req.body.code
  fs.writeFile("../authCode/authCode.txt", result, erro => {
    res.render('index',{info: 'Código submetido!'})
  })

})

module.exports = router;
