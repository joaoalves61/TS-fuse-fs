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
  var code = req.body.code
  const nonce = nacl.randomBytes(24)
  const secretKey = Buffer.from('ts_2018_grupo6_tp3_ts_2018_grupo','utf8')
  const secretData = Buffer.from(code,'utf8')
  const encryptedData =  nacl.secretbox(secretData,nonce,secretKey)
  var nonce_base64 = encodeBase64(nonce)
  var encryptedData_base64 = encodeBase64(encryptedData)
  var result = '' + nonce_base64 + ':' + encryptedData_base64
  fs.writeFile("../authCode/authCode.txt", result, erro => {
    res.render('index',{info: 'Código submetido!'})
  })

})

module.exports = router;
