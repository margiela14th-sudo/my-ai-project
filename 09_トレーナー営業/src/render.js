// 使い方: node src/render.js <htmlファイル> <pdfファイル>
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
await p.goto('file://'+path.resolve(process.argv[2]));
await p.pdf({path:process.argv[3],width:'1280px',height:'720px',printBackground:true});await b.close();})();
