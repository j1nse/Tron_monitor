const TronWeb = require('tronweb')
const fs = require("fs")
const HttpProvider = TronWeb.providers.HttpProvider; // Optional provider, can just use a url for the nodes instead

const fullNode = new HttpProvider('https://api.trongrid.io'); // Full node http endpoint
    
const solidityNode = new HttpProvider('https://api.trongrid.io'); // Solidity node http endpoint
    
const eventServer = 'https://api.trongrid.io'; // Contract events http endpoint
const privateKey = 'da146374a75310b9666e834ee4a...c76217c5a495fff9f0d0';

const tronWeb = new TronWeb(
  fullNode,
  solidityNode,
  eventServer,
  privateKey
);
var a='';

tronWeb.trx.getBlockRange(10,20).then((_a)=>{console.log(_a['transactions'][0]['ret'])});
fs.writeFile("block.txt",a.toString(), (error) =>{});
